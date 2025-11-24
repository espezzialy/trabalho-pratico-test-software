"""Testes unitários para o módulo manager.py."""

import pytest
import json
import os

from taskcrafter.manager import TaskManager
from taskcrafter.models import Task


class TestTaskManagerBasics:
    """Testes básicos do TaskManager."""
    
    def test_criar_task_manager(self, temp_data_file):
        """Teste 19: Criar TaskManager com arquivo temporário."""
        manager = TaskManager(temp_data_file)
        assert manager.tasks == []
        assert manager.data_file.exists()
    
    def test_adicionar_tarefa(self, task_manager):
        """Teste 20: Adicionar tarefa ao gerenciador."""
        task = task_manager.add_task("Minha Tarefa", "Descrição")
        assert len(task_manager.tasks) == 1
        assert task.titulo == "Minha Tarefa"
        assert task.descricao == "Descrição"
    
    def test_adicionar_tarefa_titulo_duplicado(self, task_manager):
        """Teste 21: Não deve permitir títulos duplicados."""
        task_manager.add_task("Tarefa Única")
        with pytest.raises(ValueError, match="Já existe uma tarefa com o título"):
            task_manager.add_task("Tarefa Única")
    
    def test_buscar_tarefa_por_titulo(self, task_manager_with_tasks):
        """Teste 22: Buscar tarefa pelo título."""
        task = task_manager_with_tasks.get_task_by_title("Estudar Python")
        assert task is not None
        assert task.titulo == "Estudar Python"
    
    def test_buscar_tarefa_inexistente(self, task_manager):
        """Teste 23: Buscar tarefa que não existe retorna None."""
        task = task_manager.get_task_by_title("Não Existe")
        assert task is None
    
    def test_buscar_case_insensitive(self, task_manager_with_tasks):
        """Teste 24: Busca deve ser case-insensitive."""
        task = task_manager_with_tasks.get_task_by_title("estudar python")
        assert task is not None
        assert task.titulo == "Estudar Python"


class TestTaskManagerPersistence:
    """Testes de persistência do TaskManager."""
    
    def test_salvar_tarefas(self, task_manager, temp_data_file):
        """Teste 25: Tarefas devem ser salvas no arquivo."""
        task_manager.add_task("Tarefa 1")
        task_manager.add_task("Tarefa 2")
        
        # Verifica se arquivo foi criado
        assert os.path.exists(temp_data_file)
        
        # Verifica conteúdo
        with open(temp_data_file, 'r') as f:
            data = json.load(f)
        assert len(data) == 2
    
    def test_carregar_tarefas(self, temp_data_file):
        """Teste 26: Carregar tarefas de arquivo existente."""
        # Criar manager e adicionar tarefas
        manager1 = TaskManager(temp_data_file)
        manager1.add_task("Tarefa Persistente")
        
        # Criar novo manager com mesmo arquivo
        manager2 = TaskManager(temp_data_file)
        assert len(manager2.tasks) == 1
        assert manager2.tasks[0].titulo == "Tarefa Persistente"
    
    def test_carregar_arquivo_invalido(self, temp_data_file):
        """Teste 27: Arquivo JSON inválido deve iniciar lista vazia."""
        # Escrever JSON inválido
        with open(temp_data_file, 'w') as f:
            f.write("invalid json{")
        
        manager = TaskManager(temp_data_file)
        assert manager.tasks == []


class TestTaskManagerOperations:
    """Testes de operações CRUD."""
    
    def test_atualizar_tarefa(self, task_manager_with_tasks):
        """Teste 28: Atualizar campos de uma tarefa."""
        task = task_manager_with_tasks.update_task(
            "Estudar Python",
            descricao="Nova descrição",
            prioridade="alta"
        )
        assert task.descricao == "Nova descrição"
        assert task.prioridade == "alta"
    
    def test_atualizar_tarefa_inexistente(self, task_manager):
        """Teste 29: Atualizar tarefa inexistente deve levantar erro."""
        with pytest.raises(ValueError, match="não encontrada"):
            task_manager.update_task("Não Existe", descricao="test")
    
    def test_marcar_como_concluida(self, task_manager_with_tasks):
        """Teste 30: Marcar tarefa como concluída."""
        task = task_manager_with_tasks.mark_as_done("Estudar Python")
        assert task.status == "concluida"
        assert task.data_conclusao is not None
    
    def test_marcar_inexistente_como_concluida(self, task_manager):
        """Teste 31: Marcar tarefa inexistente como concluída deve levantar erro."""
        with pytest.raises(ValueError, match="não encontrada"):
            task_manager.mark_as_done("Não Existe")
    
    def test_deletar_tarefa(self, task_manager_with_tasks):
        """Teste 32: Deletar tarefa existente."""
        initial_count = len(task_manager_with_tasks.tasks)
        result = task_manager_with_tasks.delete_task("Estudar Python")
        assert result is True
        assert len(task_manager_with_tasks.tasks) == initial_count - 1
    
    def test_deletar_tarefa_inexistente(self, task_manager):
        """Teste 33: Deletar tarefa inexistente retorna False."""
        result = task_manager.delete_task("Não Existe")
        assert result is False


class TestTaskManagerFilters:
    """Testes de filtragem e ordenação."""
    
    def test_listar_todas_tarefas(self, task_manager_with_tasks):
        """Teste 34: Listar todas as tarefas."""
        tasks = task_manager_with_tasks.list_tasks()
        assert len(tasks) == 3
    
    def test_filtrar_por_status(self, task_manager_with_tasks):
        """Teste 35: Filtrar tarefas por status."""
        task_manager_with_tasks.mark_as_done("Estudar Python")
        tasks = task_manager_with_tasks.list_tasks(status="concluida")
        assert len(tasks) == 1
        assert tasks[0].titulo == "Estudar Python"
    
    def test_filtrar_por_prioridade(self, task_manager_with_tasks):
        """Teste 36: Filtrar tarefas por prioridade."""
        tasks = task_manager_with_tasks.list_tasks(prioridade="alta")
        assert len(tasks) == 1
        assert tasks[0].titulo == "Comprar mantimentos"
    
    def test_filtrar_por_tag(self, task_manager_with_tasks):
        """Teste 37: Filtrar tarefas por tag."""
        tasks = task_manager_with_tasks.list_tasks(tag="estudo")
        assert len(tasks) == 1
        assert tasks[0].titulo == "Estudar Python"
    
    def test_filtrar_por_vencimento(self, task_manager_with_tasks):
        """Teste 38: Filtrar tarefas por data de vencimento."""
        tasks = task_manager_with_tasks.list_tasks(vencimento="2025-11-25")
        assert len(tasks) == 1
        assert tasks[0].titulo == "Comprar mantimentos"
    
    def test_ordenar_por_prioridade(self, task_manager_with_tasks):
        """Teste 39: Ordenar tarefas por prioridade."""
        tasks = task_manager_with_tasks.list_tasks(ordenar_por="prioridade")
        # alta > media > baixa
        assert tasks[0].prioridade == "alta"
        assert tasks[1].prioridade == "media"
        assert tasks[2].prioridade == "baixa"
    
    def test_ordenar_por_titulo(self, task_manager_with_tasks):
        """Teste 40: Ordenar tarefas por título."""
        tasks = task_manager_with_tasks.list_tasks(ordenar_por="titulo")
        titulos = [t.titulo for t in tasks]
        assert titulos == sorted(titulos, key=str.lower)
    
    def test_ordenar_por_vencimento(self, task_manager):
        """Teste 41: Ordenar tarefas por vencimento."""
        task_manager.add_task("Tarefa 1", data_vencimento="2025-12-31")
        task_manager.add_task("Tarefa 2", data_vencimento="2025-11-30")
        task_manager.add_task("Tarefa 3")  # Sem vencimento
        
        tasks = task_manager.list_tasks(ordenar_por="data_vencimento")
        # Tarefas com vencimento primeiro, depois sem vencimento
        assert tasks[0].data_vencimento == "2025-11-30"
        assert tasks[1].data_vencimento == "2025-12-31"
        assert tasks[2].data_vencimento is None


class TestTaskManagerStatistics:
    """Testes de estatísticas."""
    
    def test_estatisticas_vazio(self, task_manager):
        """Teste 42: Estatísticas com manager vazio."""
        stats = task_manager.get_statistics()
        assert stats["total"] == 0
        assert stats["pendentes"] == 0
    
    def test_estatisticas_completas(self, task_manager_with_tasks):
        """Teste 43: Estatísticas com tarefas."""
        task_manager_with_tasks.mark_as_done("Estudar Python")
        task_manager_with_tasks.update_task("Fazer exercícios", status="andamento")
        
        stats = task_manager_with_tasks.get_statistics()
        assert stats["total"] == 3
        assert stats["pendentes"] == 1
        assert stats["em_andamento"] == 1
        assert stats["concluidas"] == 1
        assert stats["por_prioridade"]["alta"] == 1
        assert stats["por_prioridade"]["media"] == 1
        assert stats["por_prioridade"]["baixa"] == 1
