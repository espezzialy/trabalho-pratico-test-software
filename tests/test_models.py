"""Testes unitários para o módulo models.py."""

import pytest
from datetime import datetime

from taskcrafter.models import Task


class TestTaskCreation:
    """Testes de criação de tarefas."""
    
    def test_criar_tarefa_basica(self):
        """Teste 1: Criar tarefa com apenas título."""
        task = Task(titulo="Minha Tarefa")
        assert task.titulo == "Minha Tarefa"
        assert task.descricao == ""
        assert task.prioridade == "media"
        assert task.status == "pendente"
        assert task.tags == []
        assert task.data_vencimento is None
        assert task.data_conclusao is None
    
    def test_criar_tarefa_completa(self):
        """Teste 2: Criar tarefa com todos os campos."""
        task = Task(
            titulo="Tarefa Completa",
            descricao="Descrição detalhada",
            prioridade="alta",
            status="andamento",
            tags=["importante", "urgente"],
            data_vencimento="2025-12-31"
        )
        assert task.titulo == "Tarefa Completa"
        assert task.descricao == "Descrição detalhada"
        assert task.prioridade == "alta"
        assert task.status == "andamento"
        assert task.tags == ["importante", "urgente"]
        assert task.data_vencimento == "2025-12-31"
    
    def test_data_criacao_automatica(self):
        """Teste 3: Verificar que data_criacao é gerada automaticamente."""
        task = Task(titulo="Test")
        assert task.data_criacao is not None
        # Verifica formato ISO 8601
        datetime.fromisoformat(task.data_criacao)
    
    def test_titulo_com_espacos_removidos(self):
        """Teste 4: Título com espaços extras deve ser normalizado."""
        task = Task(titulo="  Título com espaços  ")
        assert task.titulo == "Título com espaços"


class TestTaskValidation:
    """Testes de validação de tarefas."""
    
    def test_titulo_vazio_levanta_erro(self):
        """Teste 5: Título vazio deve levantar ValueError."""
        with pytest.raises(ValueError, match="T[ií]tulo n[ãa]o pode ser vazio"):
            Task(titulo="")
    
    def test_titulo_apenas_espacos_levanta_erro(self):
        """Teste 6: Título só com espaços deve levantar ValueError."""
        with pytest.raises(ValueError, match="T[ií]tulo n[ãa]o pode ser vazio"):
            Task(titulo="   ")
    
    def test_prioridade_invalida_levanta_erro(self):
        """Teste 7: Prioridade inválida deve levantar ValueError."""
        with pytest.raises(ValueError, match="Prioridade inv[áa]lida"):
            Task(titulo="Test", prioridade="urgente")
    
    def test_status_invalido_levanta_erro(self):
        """Teste 8: Status inválido deve levantar ValueError."""
        with pytest.raises(ValueError, match="Status inv[áa]lido"):
            Task(titulo="Test", status="pausada")
    
    def test_data_vencimento_formato_invalido(self):
        """Teste 9: Data de vencimento em formato inválido deve levantar erro."""
        with pytest.raises(ValueError, match="Data de vencimento deve estar no formato YYYY-MM-DD"):
            Task(titulo="Test", data_vencimento="31/12/2025")
    
    def test_data_vencimento_invalida(self):
        """Teste 10: Data de vencimento inválida deve levantar erro."""
        with pytest.raises(ValueError, match="Data de vencimento deve estar no formato YYYY-MM-DD"):
            Task(titulo="Test", data_vencimento="2025-13-45")
    
    def test_prioridades_validas(self):
        """Teste 11: Todas as prioridades válidas devem funcionar."""
        for prioridade in ["baixa", "media", "alta"]:
            task = Task(titulo=f"Test {prioridade}", prioridade=prioridade)
            assert task.prioridade == prioridade
    
    def test_status_validos(self):
        """Teste 12: Todos os status válidos devem funcionar."""
        for status in ["pendente", "andamento", "concluida"]:
            task = Task(titulo=f"Test {status}", status=status)
            assert task.status == status


class TestTaskSerialization:
    """Testes de serialização de tarefas."""
    
    def test_to_dict(self, sample_task):
        """Teste 13: Converter tarefa para dicionário."""
        task_dict = sample_task.to_dict()
        assert task_dict["titulo"] == "Tarefa de Teste"
        assert task_dict["descricao"] == "Esta é uma tarefa de teste"
        assert task_dict["prioridade"] == "media"
        assert task_dict["tags"] == ["teste", "exemplo"]
        assert task_dict["data_vencimento"] == "2025-12-31"
    
    def test_from_dict(self):
        """Teste 14: Criar tarefa a partir de dicionário."""
        data = {
            "titulo": "Nova Tarefa",
            "descricao": "Descrição",
            "prioridade": "alta",
            "status": "pendente",
            "tags": ["tag1"],
            "data_criacao": "2025-01-01T10:00:00",
            "data_vencimento": "2025-12-31",
            "data_conclusao": None
        }
        task = Task.from_dict(data)
        assert task.titulo == "Nova Tarefa"
        assert task.prioridade == "alta"
        assert task.tags == ["tag1"]
    
    def test_roundtrip_serialization(self, sample_task):
        """Teste 15: Serializar e desserializar deve manter os dados."""
        task_dict = sample_task.to_dict()
        restored_task = Task.from_dict(task_dict)
        assert restored_task.titulo == sample_task.titulo
        assert restored_task.descricao == sample_task.descricao
        assert restored_task.prioridade == sample_task.prioridade
        assert restored_task.tags == sample_task.tags


class TestTaskString:
    """Testes de representação em string."""
    
    def test_str_tarefa_simples(self):
        """Teste 16: String representation de tarefa simples."""
        task = Task(titulo="Test")
        result = str(task)
        assert "PENDENTE" in result
        assert "Test" in result
        assert "media" in result
    
    def test_str_tarefa_com_tags(self):
        """Teste 17: String representation com tags."""
        task = Task(titulo="Test", tags=["tag1", "tag2"])
        result = str(task)
        assert "tag1" in result
        assert "tag2" in result
    
    def test_str_tarefa_com_vencimento(self):
        """Teste 18: String representation com data de vencimento."""
        task = Task(titulo="Test", data_vencimento="2025-12-31")
        result = str(task)
        assert "2025-12-31" in result
        assert "vence" in result.lower()
