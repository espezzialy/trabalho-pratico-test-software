"""Modelos de dados para o TaskCrafter CLI.

Este módulo define a estrutura de dados de uma tarefa.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import json


@dataclass
class Task:
    """Representa uma tarefa no sistema TaskCrafter.
    
    Attributes:
        titulo: Título único da tarefa (obrigatório)
        descricao: Descrição detalhada da tarefa
        prioridade: Nível de prioridade (baixa, media, alta)
        status: Estado atual (pendente, andamento, concluida)
        tags: Lista de tags para categorização
        data_criacao: Data/hora de criação (ISO 8601)
        data_vencimento: Data de vencimento no formato YYYY-MM-DD
        data_conclusao: Data/hora de conclusão (ISO 8601)
    """
    
    titulo: str
    descricao: str = ""
    prioridade: str = "media"
    status: str = "pendente"
    tags: List[str] = field(default_factory=list)
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())
    data_vencimento: Optional[str] = None
    data_conclusao: Optional[str] = None
    
    def __post_init__(self):
        """Valida os dados da tarefa após inicialização."""
        self._validar_titulo()
        self._validar_prioridade()
        self._validar_status()
        self._validar_data_vencimento()
    
    def _validar_titulo(self):
        """Valida se o título não está vazio."""
        if not self.titulo or not self.titulo.strip():
            raise ValueError("Título não pode ser vazio")
        self.titulo = self.titulo.strip()
    
    def _validar_prioridade(self):
        """Valida se a prioridade é válida."""
        prioridades_validas = ["baixa", "media", "alta"]
        if self.prioridade not in prioridades_validas:
            raise ValueError(
                f"Prioridade inválida. Use: {', '.join(prioridades_validas)}"
            )
    
    def _validar_status(self):
        """Valida se o status é válido."""
        status_validos = ["pendente", "andamento", "concluida"]
        if self.status not in status_validos:
            raise ValueError(
                f"Status inválido. Use: {', '.join(status_validos)}"
            )
    
    def _validar_data_vencimento(self):
        """Valida se a data de vencimento está no formato correto."""
        if self.data_vencimento:
            try:
                datetime.strptime(self.data_vencimento, "%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    "Data de vencimento deve estar no formato YYYY-MM-DD"
                )
    
    def to_dict(self) -> dict:
        """Converte a tarefa para dicionário.
        
        Returns:
            Dicionário com os dados da tarefa
        """
        return {
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prioridade": self.prioridade,
            "status": self.status,
            "tags": self.tags,
            "data_criacao": self.data_criacao,
            "data_vencimento": self.data_vencimento,
            "data_conclusao": self.data_conclusao
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Cria uma tarefa a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados da tarefa
            
        Returns:
            Instância de Task
        """
        return cls(**data)
    
    def __str__(self) -> str:
        """Representação em string da tarefa."""
        tags_str = f" [{', '.join(self.tags)}]" if self.tags else ""
        vencimento_str = f" (vence: {self.data_vencimento})" if self.data_vencimento else ""
        return f"[{self.status.upper()}] {self.titulo} - {self.prioridade}{tags_str}{vencimento_str}"
