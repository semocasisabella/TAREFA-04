import unittest

from sistema_alunos import CadastroAlunos


class CadastroAlunosTests(unittest.TestCase):
    def setUp(self):
        self.cadastro = CadastroAlunos()
        self.aluno = self.cadastro.cadastrar(
            "25100003", "Pedro Oliveira", "Rua XV de Novembro, 100",
            "10/05/2006",
        )

    def test_recusa_matricula_duplicada(self):
        with self.assertRaisesRegex(ValueError, "matrícula"):
            self.cadastro.cadastrar(
                "25100003", "Outra pessoa", "Rua B, 2", "01/01/2000"
            )

    def test_recusa_data_invalida(self):
        with self.assertRaisesRegex(ValueError, "Data inválida"):
            self.cadastro.cadastrar(
                "25100004", "Outra pessoa", "Rua B, 2", "31/02/2000"
            )

    def test_busca_por_nome_ou_matricula(self):
        self.assertEqual(self.cadastro.buscar("pedro"), [self.aluno])
        self.assertEqual(self.cadastro.buscar("25100003"), [self.aluno])

    def test_altera_e_exclui_aluno(self):
        atualizado = self.cadastro.alterar(
            "25100003", "25100004", "Pedro Oliveira", "Rua A, 1",
            "10/05/2006",
        )
        self.assertIs(atualizado, self.aluno)
        self.assertEqual(self.cadastro.buscar_matricula("25100004"), self.aluno)
        self.assertIsNone(self.cadastro.buscar_matricula("25100003"))

        removido = self.cadastro.excluir("25100004")
        self.assertIs(removido, self.aluno)
        self.assertEqual(self.cadastro.alunos, [])


if __name__ == "__main__":
    unittest.main()
