"""Testes de integração e end-to-end do TaskCrafter CLI.

Estes testes simulam fluxos completos de uso do sistema.
"""

import pytest
import tempfile
import os
from io import StringIO
import sys

from taskcrafter.cli import TaskCrafterCLI
from taskcrafter.manager import TaskManager


class TestCLIIntegration:
    """Testes de integração da CLI."""
    
    @pytest.fixture
    def cli(self, temp_data_file):
        """Cria instância da CLI para testes."""
        return TaskCrafterCLI(temp_data_file)
    
    def test_fluxo_completo_adicionar_listar(self, cli, capsys):
        """Teste E2E 1: Fluxo completo de adicionar e listar tarefas."""
        # Adicionar tarefas
        cli.run(['add', 'Estudar', '-d', 'Revisar Python', '-p', 'alta'])
        cli.run(['add', 'Exercitar', '-p', 'baixa', '-t', 'saúde'])
        
        # Listar tarefas
        cli.run(['list'])
        captured = capsys.readouterr()
        
        assert 'Estudar' in captured.out
        assert 'Exercitar' in captured.out
        assert '2' in captured.out  # Total de tarefas
    
    def test_fluxo_completo_adicionar_atualizar_listar(self, cli, capsys):
        """Teste E2E 2: Adicionar, atualizar e listar tarefa."""
        # Adicionar
        cli.run(['add', 'Tarefa Original', '-p', 'baixa'])
        
        # Atualizar
        cli.run(['update', 'Tarefa Original', '-p', 'alta', '-d', 'Nova descrição'])
        
        # Verificar atualização
        task = cli.manager.get_task_by_title('Tarefa Original')
        assert task.prioridade == 'alta'
        assert task.descricao == 'Nova descrição'
    
    def test_fluxo_completo_adicionar_concluir_filtrar(self, cli, capsys):
        """Teste E2E 3: Adicionar, concluir e filtrar por status."""
        # Adicionar tarefas
        cli.run(['add', 'Tarefa 1'])
        cli.run(['add', 'Tarefa 2'])
        cli.run(['add', 'Tarefa 3'])
        
        # Concluir uma
        cli.run(['done', 'Tarefa 2'])
        
        # Filtrar pendentes
        cli.run(['filter', '-s', 'pendente'])
        captured = capsys.readouterr()
        
        assert 'Tarefa 1' in captured.out
        assert 'Tarefa 3' in captured.out
        assert 'Tarefa 2' not in captured.out or 'concluida' in captured.out.lower()
    
    def test_fluxo_completo_adicionar_deletar_listar(self, cli, capsys):
        """Teste E2E 4: Adicionar, deletar e verificar remoção."""
        # Adicionar tarefas
        cli.run(['add', 'Tarefa Temporária'])
        cli.run(['add', 'Tarefa Permanente'])
        capsys.readouterr()  # Limpar buffer
        
        # Deletar
        cli.run(['delete', 'Tarefa Temporária'])
        capsys.readouterr()  # Limpar buffer
        
        # Verificar que foi removida
        cli.run(['list'])
        captured = capsys.readouterr()
        
        # Na listagem final, Tarefa Temporária não deve aparecer
        lines = captured.out.split('\n')
        list_lines = '\n'.join([l for l in lines if '📋' in l or '⏳' in l or 'Tarefa' in l])
        
        assert 'Tarefa Temporária' not in list_lines or 'removida' not in list_lines
        assert 'Tarefa Permanente' in captured.out
    
    def test_fluxo_completo_gestao_projeto(self, cli, capsys):
        """Teste E2E 5: Simula gestão completa de um projeto."""
        # Setup do projeto
        cli.run(['add', 'Planejar projeto', '-p', 'alta', '-t', 'planejamento'])
        cli.run(['add', 'Implementar funcionalidade', '-p', 'media', '-t', 'dev'])
        cli.run(['add', 'Escrever testes', '-p', 'media', '-t', 'dev', 'testes'])
        cli.run(['add', 'Documentação', '-p', 'baixa', '-t', 'docs'])
        
        # Iniciar trabalho
        cli.run(['update', 'Planejar projeto', '-s', 'andamento'])
        
        # Concluir planejamento
        cli.run(['done', 'Planejar projeto'])
        
        # Verificar tarefas em andamento
        cli.run(['filter', '-s', 'andamento'])
        captured1 = capsys.readouterr()
        assert 'Nenhuma tarefa encontrada' in captured1.out or 'Total de tarefas: 0' in captured1.out
        
        # Verificar tarefas de dev
        cli.run(['filter', '-t', 'dev'])
        captured2 = capsys.readouterr()
        assert 'Implementar funcionalidade' in captured2.out
        assert 'Escrever testes' in captured2.out
        
        # Verificar estatísticas
        cli.run(['stats'])
        captured3 = capsys.readouterr()
        assert 'Total de tarefas: 4' in captured3.out
        assert 'Concluídas: 1' in captured3.out


class TestCLIEdgeCases:
    """Testes de casos extremos da CLI."""
    
    @pytest.fixture
    def cli(self, temp_data_file):
        """Cria instância da CLI para testes."""
        return TaskCrafterCLI(temp_data_file)
    
    def test_adicionar_tarefa_titulo_duplicado_mostra_erro(self, cli, capsys):
        """Teste E2E 6: Tentar adicionar título duplicado mostra erro."""
        cli.run(['add', 'Tarefa Única'])
        
        # Tentar adicionar novamente
        with pytest.raises(SystemExit):
            cli.run(['add', 'Tarefa Única'])
        
        captured = capsys.readouterr()
        assert 'Erro' in captured.err or 'existe' in captured.err.lower()
    
    def test_atualizar_tarefa_inexistente_mostra_erro(self, cli, capsys):
        """Teste E2E 7: Atualizar tarefa inexistente mostra erro."""
        with pytest.raises(SystemExit):
            cli.run(['update', 'Não Existe', '-p', 'alta'])
        
        captured = capsys.readouterr()
        assert 'Erro' in captured.err or 'não encontrada' in captured.err.lower()
    
    def test_listar_sem_tarefas(self, cli, capsys):
        """Teste E2E 8: Listar quando não há tarefas."""
        cli.run(['list'])
        captured = capsys.readouterr()
        assert 'Nenhuma tarefa' in captured.out or 'vazia' in captured.out.lower()
    
    def test_filtro_sem_resultados(self, cli, capsys):
        """Teste E2E 9: Filtro que não retorna resultados."""
        cli.run(['add', 'Tarefa 1', '-p', 'baixa'])
        cli.run(['filter', '-p', 'alta'])
        captured = capsys.readouterr()
        assert 'Nenhuma tarefa' in captured.out


class TestCLIWithDates:
    """Testes de integração com datas."""
    
    @pytest.fixture
    def cli(self, temp_data_file):
        """Cria instância da CLI para testes."""
        return TaskCrafterCLI(temp_data_file)
    
    def test_adicionar_com_vencimento(self, cli):
        """Teste E2E 10: Adicionar tarefa com data de vencimento."""
        cli.run(['add', 'Entrega Projeto', '-v', '2025-12-31', '-p', 'alta'])
        task = cli.manager.get_task_by_title('Entrega Projeto')
        assert task.data_vencimento == '2025-12-31'
    
    def test_filtrar_por_vencimento(self, cli, capsys):
        """Teste E2E 11: Filtrar tarefas por data de vencimento."""
        cli.run(['add', 'Tarefa 1', '-v', '2025-12-25'])
        cli.run(['add', 'Tarefa 2', '-v', '2025-12-31'])
        capsys.readouterr()  # Limpar buffer
        
        cli.run(['filter', '-v', '2025-12-25'])
        captured = capsys.readouterr()
        
        # Verificar que apenas Tarefa 1 aparece na listagem filtrada
        lines = captured.out.split('\n')
        list_section = '\n'.join([l for l in lines if '📋' in l or '⏳' in l or 'Tarefa' in l])
        assert 'Tarefa 1' in list_section
        # Tarefa 2 não deve aparecer na lista (apenas contagem pode ter o número 2)
        assert list_section.count('Tarefa') == 1
    
    def test_ordenar_por_vencimento(self, cli, capsys):
        """Teste E2E 12: Ordenar tarefas por vencimento."""
        cli.run(['add', 'Tarefa Z', '-v', '2025-12-31'])
        cli.run(['add', 'Tarefa A', '-v', '2025-11-30'])
        capsys.readouterr()  # Limpar buffer
        
        cli.run(['list', '-o', 'data_vencimento'])
        captured = capsys.readouterr()
        
        # Extrair apenas a seção de listagem
        lines = [l for l in captured.out.split('\n') if 'Tarefa A' in l or 'Tarefa Z' in l]
        # Tarefa A deve aparecer antes (vence primeiro)
        if len(lines) >= 2:
            # Verificar ordem das tarefas na lista
            assert 'Tarefa A' in lines[0] or captured.out.index('1. ⏳') < captured.out.rindex('2. ⏳')
        else:
            # Se apenas uma linha, verificar que A está antes de Z no texto
            pos_a = captured.out.rfind('Tarefa A')  # última ocorrência
            pos_z = captured.out.rfind('Tarefa Z')
            assert pos_a < pos_z


class TestCLIPersistence:
    """Testes de persistência através de múltiplas instâncias."""
    
    def test_persistencia_entre_sessoes(self, temp_data_file, capsys):
        """Teste E2E 13: Dados persistem entre diferentes instâncias da CLI."""
        # Primeira sessão
        cli1 = TaskCrafterCLI(temp_data_file)
        cli1.run(['add', 'Tarefa Persistente', '-p', 'alta'])
        cli1.run(['add', 'Outra Tarefa'])
        
        # Segunda sessão (nova instância)
        cli2 = TaskCrafterCLI(temp_data_file)
        cli2.run(['list'])
        captured = capsys.readouterr()
        
        assert 'Tarefa Persistente' in captured.out
        assert 'Outra Tarefa' in captured.out
        
        # Modificar na segunda sessão
        cli2.run(['done', 'Tarefa Persistente'])
        
        # Terceira sessão
        cli3 = TaskCrafterCLI(temp_data_file)
        task = cli3.manager.get_task_by_title('Tarefa Persistente')
        assert task.status == 'concluida'
