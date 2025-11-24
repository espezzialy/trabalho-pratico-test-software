"""Fixtures compartilhadas para os testes do TaskCrafter."""

import pytest
import tempfile
import os
from pathlib import Path

from taskcrafter.manager import TaskManager
from taskcrafter.models import Task


@pytest.fixture
def temp_data_file():
    """Cria um arquivo temporário para testes.
    
    Yields:
        Caminho do arquivo temporário
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def task_manager(temp_data_file):
    """Cria um TaskManager com arquivo temporário.
    
    Args:
        temp_data_file: Fixture do arquivo temporário
        
    Returns:
        TaskManager inicializado
    """
    return TaskManager(temp_data_file)


@pytest.fixture
def sample_task():
    """Cria uma tarefa de exemplo para testes.
    
    Returns:
        Task de exemplo
    """
    return Task(
        titulo="Tarefa de Teste",
        descricao="Esta é uma tarefa de teste",
        prioridade="media",
        tags=["teste", "exemplo"],
        data_vencimento="2025-12-31"
    )


@pytest.fixture
def task_manager_with_tasks(task_manager):
    """Cria um TaskManager com algumas tarefas pré-cadastradas.
    
    Args:
        task_manager: Fixture do TaskManager
        
    Returns:
        TaskManager com tarefas
    """
    task_manager.add_task("Comprar mantimentos", "Ir ao supermercado", "alta", ["casa", "urgente"], "2025-11-25")
    task_manager.add_task("Estudar Python", "Revisar conceitos de OOP", "media", ["estudo"])
    task_manager.add_task("Fazer exercícios", "30 minutos de caminhada", "baixa", ["saúde"])
    return task_manager
