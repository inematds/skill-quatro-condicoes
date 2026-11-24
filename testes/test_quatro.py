"""Testes do quatro.py — rodam sem modelo (QUATRO_FALSO=1). python3 -m unittest discover testes"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import quatro  # noqa: E402


class TestSistema(unittest.TestCase):
    def test_cada_condicao_recebe_so_o_seu(self):
        self.assertEqual(quatro.texto_sistema("nada", "CM", "SK"), "")
        self.assertIn("CM", quatro.texto_sistema("claudemd", "CM", "SK"))
        self.assertNotIn("SK", quatro.texto_sistema("claudemd", "CM", "SK"))
        self.assertIn("SK", quatro.texto_sistema("skill", "CM", "SK"))
        self.assertNotIn("CM", quatro.texto_sistema("skill", "CM", "SK"))
        t = quatro.texto_sistema("ambos", "CM", "SK")
        self.assertIn("CM", t)
        self.assertIn("SK", t)

    def test_limite_de_tamanho(self):
        with self.assertRaises(SystemExit):
            quatro.texto_sistema("claudemd", "x" * (quatro.LIMITE_SISTEMA + 1), "")

    def test_comando_isola_e_nao_libera_bash(self):
        cmd = quatro.comando_claude("sonnet", "", False)
        self.assertIn("--safe-mode", cmd)
        self.assertIn("--disable-slash-commands", cmd)
        self.assertNotIn("Bash", cmd[cmd.index("--allowedTools") + 1])
        self.assertNotIn("--append-system-prompt", cmd)
        self.assertIn("Bash", quatro.comando_claude("sonnet", "x", True)[cmd.index("--allowedTools") + 1])


class TestJuiz(unittest.TestCase):
    def test_embaralhar_reprodutivel_e_completo(self):
        regs = [{"condicao": c} for c in quatro.CONDICOES]
        a = quatro.embaralhar(regs, 7)
        b = quatro.embaralhar(regs, 7)
        self.assertEqual([r["condicao"] for _, r in a], [r["condicao"] for _, r in b])
        self.assertEqual(sorted(r["condicao"] for _, r in a), sorted(quatro.CONDICOES))
        self.assertEqual([l for l, _ in a], list("ABCD"))

    def test_prompt_nao_revela_condicao(self):
        with tempfile.TemporaryDirectory() as d:
            regs = [{"condicao": c, "resposta": "texto", "arquivos_novos": [], "pasta": d} for c in quatro.CONDICOES]
            p = quatro.prompt_juiz("tarefa", "", quatro.embaralhar(regs, 1))
            for nome in ("claudemd", "CLAUDE.md", "skill", "nada", "ambos"):
                self.assertNotIn(nome, p.split("# Formato")[0].split("## Resposta A")[1])

    def test_extrair_json_com_lixo_em_volta(self):
        self.assertEqual(quatro.extrair_json('ok\n{"notas": {"A": {"nota": 8}}}\nfim')["notas"]["A"]["nota"], 8)
        self.assertIsNone(quatro.extrair_json("sem json"))


class TestVeredito(unittest.TestCase):
    def lin(self, **n):
        return [{"condicao": c, "nota": v} for c, v in n.items()]

    def test_skill_ajuda(self):
        self.assertIn("AJUDA", quatro.veredito(self.lin(nada=5, skill=8))[0])

    def test_skill_atrapalha(self):
        self.assertIn("ATRAPALHA", quatro.veredito(self.lin(nada=8, skill=6))[0])

    def test_empate_dentro_da_margem(self):
        self.assertIn("NÃO MUDA", quatro.veredito(self.lin(nada=7, skill=7.3))[0])

    def test_conflito_quando_juntos_pioram(self):
        v = quatro.veredito(self.lin(nada=5, claudemd=7, skill=8, ambos=6))
        self.assertTrue(any("conflito" in x for x in v))

    def test_claudemd_atrapalha(self):
        v = quatro.veredito(self.lin(nada=8, claudemd=6, skill=8))
        self.assertTrue(any("CLAUDE.md ATRAPALHA" in x for x in v))


class TestRecusa(unittest.TestCase):
    def test_detecta_recusa_no_comeco(self):
        self.assertTrue(quatro.recusou("Desculpe, não posso ajudar com isso."))
        self.assertTrue(quatro.recusou("I can't help with that request."))
        self.assertFalse(quatro.recusou("Aqui está o roteiro pedido."))
        self.assertFalse(quatro.recusou("x" * 700 + " não posso fazer"))

    def test_veredito_avisa_recusa(self):
        v = quatro.veredito([{"condicao": "nada", "nota": 2, "recusas": 2}, {"condicao": "skill", "nota": 2, "recusas": 0}])
        self.assertTrue(any("RECUSA" in x for x in v))


class TestPontaAPonta(unittest.TestCase):
    def test_roda_as_4_e_escreve_relatorio(self):
        os.environ["QUATRO_FALSO"] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                d = Path(d)
                (d / "t.md").write_text("faça X")
                (d / "s.md").write_text("skill")
                (d / "c.md").write_text("regras")
                quatro.main(["--tarefa", str(d / "t.md"), "--skill", str(d / "s.md"), "--claudemd",
                             str(d / "c.md"), "--saida", str(d / "out"), "--semente", "3", "--rep", "2"])
                res = json.loads((d / "out" / "resultado.json").read_text())
                self.assertEqual(len(res["rodadas"]), 8)
                self.assertTrue(all(r["nota"] is not None for r in res["rodadas"]))
                self.assertEqual([l["condicao"] for l in res["resumo"]], quatro.CONDICOES)
                self.assertIn("Veredito", (d / "out" / "relatorio.md").read_text())
        finally:
            del os.environ["QUATRO_FALSO"]

    def test_sem_skill_roda_so_duas(self):
        os.environ["QUATRO_FALSO"] = "1"
        try:
            with tempfile.TemporaryDirectory() as d:
                d = Path(d)
                (d / "t.md").write_text("faça X")
                (d / "c.md").write_text("regras")
                quatro.main(["--tarefa", str(d / "t.md"), "--claudemd", str(d / "c.md"), "--saida", str(d / "o")])
                res = json.loads((d / "o" / "resultado.json").read_text())
                self.assertEqual(sorted({r["condicao"] for r in res["rodadas"]}), ["claudemd", "nada"])
        finally:
            del os.environ["QUATRO_FALSO"]


if __name__ == "__main__":
    unittest.main()
