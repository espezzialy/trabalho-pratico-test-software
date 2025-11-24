"""Gerenciador de tarefas do TaskCrafter CLI.

Este módulo implementa todas as operações CRUD e lógica de negócio.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from .models import Task


class TaskManager:
    """Gerenciador de tarefas com persistência em JSON.
    
    Attributes:
        data_file: Caminho para o arquivo JSON de persistência
        tasks: Lista de tarefas carregadas em memória
    """
    
    def __init__(self, data_file: str = "data/tasks.json"):
        """Inicializa o gerenciador de tarefas.
        
        Args:
            data_file: Caminho para o arquivo de dados JSON
        """
        self.data_file = Path(data_file)
        self.tasks: List[Task] = []
        self._ensure_data_directory()
        self.load_tasks()
    
    def _ensure_data_directory(self):
        """Garante que o diretório de dados existe."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
    
    def load_tasks(self):
        """Carrega tarefas do arquivo JSON."""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except (json.JSONDecodeError, Exception) as e:
                # Se houver erro ao carregar, inicia com lista vazia
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Salva tarefas no arquivo JSON."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            data = [task.to_dict() for task in self.tasks]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_task(self, titulo: str, descricao: str = "", prioridade: str = "media",
                 tags: Optional[List[str]] = None, data_vencimento: Optional[str] = None) -> Task:
        """Adiciona uma nova tarefa.
        
        Args:
            titulo: Título único da tarefa
            descricao: Descrição da tarefa
            prioridade: Prioridade (baixa, media, alta)
            tags: Lista de tags
            data_vencimento: Data de vencimento (YYYY-MM-DD)
            
        Returns:
            Tarefa criada
            
        Raises:
            ValueError: Se o título já existe ou dados inválidos
        """
        # Verifica se título já existe
        if self.get_task_by_title(titulo):
            raise ValueError(f"Já existe uma tarefa com o título '{titulo}'")
        
        # Cria a tarefa (validações ocorrem no __post_init__)
        task = Task(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            tags=tags or [],
            data_vencimento=data_vencimento
        )
        
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def get_task_by_title(self, titulo: str) -> Optional[Task]:
        """Busca uma tarefa pelo título.
        
        Args:
            titulo: Título da tarefa
            
        Returns:
            Tarefa encontrada ou None
        """
        for task in self.tasks:
            if task.titulo.lower() == titulo.lower():
                return task
        return None
    
    def list_tasks(self, status: Optional[str] = None, prioridade: Optional[str] = None,
                   tag: Optional[str] = None, vencimento: Optional[str] = None,
                   ordenar_por: str = "data_criacao") -> List[Task]:
        """Lista tarefas com filtros e ordenação.
        
        Args:
            status: Filtrar por status (pendente, andamento, concluida)
            prioridade: Filtrar por prioridade (baixa, media, alta)
            tag: Filtrar por tag
            vencimento: Filtrar por data de vencimento (YYYY-MM-DD)
            ordenar_por: Campo para ordenação (data_criacao, prioridade, titulo, data_vencimento)
            
        Returns:
            Lista de tarefas filtradas e ordenadas
        """
        filtered_tasks = self.tasks.copy()
        
        # Aplicar filtros
        if status:
            filtered_tasks = [t for t in filtered_tasks if t.status == status]
        
        if prioridade:
            filtered_tasks = [t for t in filtered_tasks if t.prioridade == prioridade]
        
        if tag:
            filtered_tasks = [t for t in filtered_tasks if tag in t.tags]
        
        if vencimento:
            filtered_tasks = [t for t in filtered_tasks if t.data_vencimento == vencimento]
        
        # Ordenar
        if ordenar_por == "prioridade":
            # Ordem: alta > media > baixa
            prioridade_ordem = {"alta": 0, "media": 1, "baixa": 2}
            filtered_tasks.sort(key=lambda t: prioridade_ordem.get(t.prioridade, 3))
        elif ordenar_por == "titulo":
            filtered_tasks.sort(key=lambda t: t.titulo.lower())
        elif ordenar_por == "data_vencimento":
            # Tarefas sem vencimento vão para o final
            filtered_tasks.sort(key=lambda t: (t.data_vencimento is None, t.data_vencimento))
        else:  # data_criacao (padrão)
            filtered_tasks.sort(key=lambda t: t.data_criacao)
        
        return filtered_tasks
    
    def update_task(self, titulo: str, **kwargs) -> Task:
        """Atualiza uma tarefa existente.
        
        Args:
            titulo: Título da tarefa a atualizar
            **kwargs: Campos a atualizar (descricao, prioridade, status, tags, data_vencimento)
            
        Returns:
            Tarefa atualizada
            
        Raises:
            ValueError: Se a tarefa não existe ou dados inválidos
        """
        task = self.get_task_by_title(titulo)
        if not task:
            raise ValueError(f"Tarefa '{titulo}' não encontrada")
        
        # Atualizar campos permitidos
        allowed_fields = ['descricao', 'prioridade', 'status', 'tags', 'data_vencimento']
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(task, field, value)
        
        # Revalidar a tarefa
        task.__post_init__()
        
        self.save_tasks()
        return task
    
    def mark_as_done(self, titulo: str) -> Task:
        """Marca uma tarefa como concluída.
        
        Args:
            titulo: Título da tarefa
            
        Returns:
            Tarefa atualizada
            
        Raises:
            ValueError: Se a tarefa não existe
        """
        task = self.get_task_by_title(titulo)
        if not task:
            raise ValueError(f"Tarefa '{titulo}' não encontrada")
        
        task.status = "concluida"
        task.data_conclusao = datetime.now().isoformat()
        
        self.save_tasks()
        return task
    
    def delete_task(self, titulo: str) -> bool:
        """Remove uma tarefa.
        
        Args:
            titulo: Título da tarefa
            
        Returns:
            True se removida, False se não encontrada
        """
        task = self.get_task_by_title(titulo)
        if not task:
            return False
        
        self.tasks.remove(task)
        self.save_tasks()
        return True
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas sobre as tarefas.
        
        Returns:
            Dicionário com estatísticas
        """
        total = len(self.tasks)
        if total == 0:
            return {
                "total": 0,
                "pendentes": 0,
                "em_andamento": 0,
                "concluidas": 0,
                "por_prioridade": {"baixa": 0, "media": 0, "alta": 0}
            }
        
        stats = {
            "total": total,
            "pendentes": len([t for t in self.tasks if t.status == "pendente"]),
            "em_andamento": len([t for t in self.tasks if t.status == "andamento"]),
            "concluidas": len([t for t in self.tasks if t.status == "concluida"]),
            "por_prioridade": {
                "baixa": len([t for t in self.tasks if t.prioridade == "baixa"]),
                "media": len([t for t in self.tasks if t.prioridade == "media"]),
                "alta": len([t for t in self.tasks if t.prioridade == "alta"])
            }
        }
        
        return stats
