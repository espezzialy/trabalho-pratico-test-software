"""Interface CLI do TaskCrafter usando argparse.

Este módulo implementa a interface de linha de comando para todas as operações.
"""

import argparse
import sys
from typing import List, Optional

from .manager import TaskManager
from . import __version__, __author__


class TaskCrafterCLI:
    """Interface de linha de comando para o TaskCrafter."""
    
    def __init__(self, data_file: str = "data/tasks.json"):
        """Inicializa a CLI.
        
        Args:
            data_file: Caminho para o arquivo de dados
        """
        self.manager = TaskManager(data_file)
    
    def run(self, args: Optional[List[str]] = None):
        """Executa a CLI com os argumentos fornecidos.
        
        Args:
            args: Lista de argumentos (usa sys.argv se None)
        """
        parser = self._create_parser()
        
        if args is None:
            args = sys.argv[1:]
        
        parsed_args = parser.parse_args(args)
        
        # Se nenhum comando foi especificado, mostra ajuda
        if not hasattr(parsed_args, 'func'):
            parser.print_help()
            return
        
        try:
            parsed_args.func(parsed_args)
        except ValueError as e:
            print(f"❌ Erro: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"❌ Erro inesperado: {e}", file=sys.stderr)
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Cria o parser de argumentos principal.
        
        Returns:
            ArgumentParser configurado
        """
        parser = argparse.ArgumentParser(
            prog='taskcrafter',
            description=f'TaskCrafter CLI - Sistema de Gerenciamento de Tarefas v{__version__}',
            epilog=f'Desenvolvido por: {__author__}'
        )
        
        parser.add_argument(
            '--version',
            action='version',
            version=f'TaskCrafter CLI v{__version__}'
        )
        
        subparsers = parser.add_subparsers(title='comandos', dest='command')
        
        # Comando: add
        self._add_add_parser(subparsers)
        
        # Comando: list
        self._add_list_parser(subparsers)
        
        # Comando: update
        self._add_update_parser(subparsers)
        
        # Comando: done
        self._add_done_parser(subparsers)
        
        # Comando: delete
        self._add_delete_parser(subparsers)
        
        # Comando: filter
        self._add_filter_parser(subparsers)
        
        # Comando: stats
        self._add_stats_parser(subparsers)
        
        return parser
    
    def _add_add_parser(self, subparsers):
        """Adiciona o parser do comando 'add'."""
        add_parser = subparsers.add_parser(
            'add',
            help='Adiciona uma nova tarefa'
        )
        add_parser.add_argument(
            'titulo',
            help='Título único da tarefa'
        )
        add_parser.add_argument(
            '-d', '--descricao',
            default='',
            help='Descrição detalhada da tarefa'
        )
        add_parser.add_argument(
            '-p', '--prioridade',
            choices=['baixa', 'media', 'alta'],
            default='media',
            help='Prioridade da tarefa (padrão: media)'
        )
        add_parser.add_argument(
            '-t', '--tags',
            nargs='+',
            default=[],
            help='Tags para categorização'
        )
        add_parser.add_argument(
            '-v', '--vencimento',
            help='Data de vencimento no formato YYYY-MM-DD'
        )
        add_parser.set_defaults(func=self._cmd_add)
    
    def _add_list_parser(self, subparsers):
        """Adiciona o parser do comando 'list'."""
        list_parser = subparsers.add_parser(
            'list',
            help='Lista todas as tarefas'
        )
        list_parser.add_argument(
            '-s', '--status',
            choices=['pendente', 'andamento', 'concluida'],
            help='Filtrar por status'
        )
        list_parser.add_argument(
            '-p', '--prioridade',
            choices=['baixa', 'media', 'alta'],
            help='Filtrar por prioridade'
        )
        list_parser.add_argument(
            '-t', '--tag',
            help='Filtrar por tag'
        )
        list_parser.add_argument(
            '-o', '--ordenar',
            choices=['data_criacao', 'prioridade', 'titulo', 'data_vencimento'],
            default='data_criacao',
            help='Ordenar por campo (padrão: data_criacao)'
        )
        list_parser.set_defaults(func=self._cmd_list)
    
    def _add_update_parser(self, subparsers):
        """Adiciona o parser do comando 'update'."""
        update_parser = subparsers.add_parser(
            'update',
            help='Atualiza uma tarefa existente'
        )
        update_parser.add_argument(
            'titulo',
            help='Título da tarefa a atualizar'
        )
        update_parser.add_argument(
            '-d', '--descricao',
            help='Nova descrição'
        )
        update_parser.add_argument(
            '-p', '--prioridade',
            choices=['baixa', 'media', 'alta'],
            help='Nova prioridade'
        )
        update_parser.add_argument(
            '-s', '--status',
            choices=['pendente', 'andamento', 'concluida'],
            help='Novo status'
        )
        update_parser.add_argument(
            '-t', '--tags',
            nargs='+',
            help='Novas tags (substitui as existentes)'
        )
        update_parser.add_argument(
            '-v', '--vencimento',
            help='Nova data de vencimento (YYYY-MM-DD)'
        )
        update_parser.set_defaults(func=self._cmd_update)
    
    def _add_done_parser(self, subparsers):
        """Adiciona o parser do comando 'done'."""
        done_parser = subparsers.add_parser(
            'done',
            help='Marca uma tarefa como concluída'
        )
        done_parser.add_argument(
            'titulo',
            help='Título da tarefa'
        )
        done_parser.set_defaults(func=self._cmd_done)
    
    def _add_delete_parser(self, subparsers):
        """Adiciona o parser do comando 'delete'."""
        delete_parser = subparsers.add_parser(
            'delete',
            help='Remove uma tarefa'
        )
        delete_parser.add_argument(
            'titulo',
            help='Título da tarefa'
        )
        delete_parser.set_defaults(func=self._cmd_delete)
    
    def _add_filter_parser(self, subparsers):
        """Adiciona o parser do comando 'filter'."""
        filter_parser = subparsers.add_parser(
            'filter',
            help='Filtra tarefas por múltiplos critérios'
        )
        filter_parser.add_argument(
            '-s', '--status',
            choices=['pendente', 'andamento', 'concluida'],
            help='Filtrar por status'
        )
        filter_parser.add_argument(
            '-p', '--prioridade',
            choices=['baixa', 'media', 'alta'],
            help='Filtrar por prioridade'
        )
        filter_parser.add_argument(
            '-t', '--tag',
            help='Filtrar por tag'
        )
        filter_parser.add_argument(
            '-v', '--vencimento',
            help='Filtrar por data de vencimento (YYYY-MM-DD)'
        )
        filter_parser.add_argument(
            '-o', '--ordenar',
            choices=['data_criacao', 'prioridade', 'titulo', 'data_vencimento'],
            default='data_criacao',
            help='Ordenar por campo (padrão: data_criacao)'
        )
        filter_parser.set_defaults(func=self._cmd_filter)
    
    def _add_stats_parser(self, subparsers):
        """Adiciona o parser do comando 'stats'."""
        stats_parser = subparsers.add_parser(
            'stats',
            help='Mostra estatísticas das tarefas'
        )
        stats_parser.set_defaults(func=self._cmd_stats)
    
    # Implementação dos comandos
    
    def _cmd_add(self, args):
        """Executa o comando add."""
        task = self.manager.add_task(
            titulo=args.titulo,
            descricao=args.descricao,
            prioridade=args.prioridade,
            tags=args.tags,
            data_vencimento=args.vencimento
        )
        print(f"✅ Tarefa criada: {task}")
    
    def _cmd_list(self, args):
        """Executa o comando list."""
        tasks = self.manager.list_tasks(
            status=args.status,
            prioridade=args.prioridade,
            tag=args.tag,
            ordenar_por=args.ordenar
        )
        
        if not tasks:
            print("📭 Nenhuma tarefa encontrada")
            return
        
        print(f"\n📋 Total de tarefas: {len(tasks)}\n")
        for i, task in enumerate(tasks, 1):
            self._print_task(i, task)
    
    def _cmd_update(self, args):
        """Executa o comando update."""
        updates = {}
        if args.descricao is not None:
            updates['descricao'] = args.descricao
        if args.prioridade is not None:
            updates['prioridade'] = args.prioridade
        if args.status is not None:
            updates['status'] = args.status
        if args.tags is not None:
            updates['tags'] = args.tags
        if args.vencimento is not None:
            updates['data_vencimento'] = args.vencimento
        
        if not updates:
            print("⚠️  Nenhuma atualização fornecida")
            return
        
        task = self.manager.update_task(args.titulo, **updates)
        print(f"✅ Tarefa atualizada: {task}")
    
    def _cmd_done(self, args):
        """Executa o comando done."""
        task = self.manager.mark_as_done(args.titulo)
        print(f"✅ Tarefa concluída: {task}")
    
    def _cmd_delete(self, args):
        """Executa o comando delete."""
        if self.manager.delete_task(args.titulo):
            print(f"✅ Tarefa '{args.titulo}' removida com sucesso")
        else:
            print(f"❌ Tarefa '{args.titulo}' não encontrada")
    
    def _cmd_filter(self, args):
        """Executa o comando filter."""
        tasks = self.manager.list_tasks(
            status=args.status,
            prioridade=args.prioridade,
            tag=args.tag,
            vencimento=args.vencimento,
            ordenar_por=args.ordenar
        )
        
        if not tasks:
            print("📭 Nenhuma tarefa encontrada com os filtros especificados")
            return
        
        print(f"\n📋 Total de tarefas: {len(tasks)}\n")
        for i, task in enumerate(tasks, 1):
            self._print_task(i, task)
    
    def _cmd_stats(self, args):
        """Executa o comando stats."""
        stats = self.manager.get_statistics()
        
        print("\n📊 Estatísticas das Tarefas\n")
        print(f"Total de tarefas: {stats['total']}")
        print(f"\n📌 Por status:")
        print(f"  • Pendentes: {stats['pendentes']}")
        print(f"  • Em andamento: {stats['em_andamento']}")
        print(f"  • Concluídas: {stats['concluidas']}")
        print(f"\n🎯 Por prioridade:")
        print(f"  • Baixa: {stats['por_prioridade']['baixa']}")
        print(f"  • Média: {stats['por_prioridade']['media']}")
        print(f"  • Alta: {stats['por_prioridade']['alta']}")
    
    def _print_task(self, index: int, task):
        """Imprime uma tarefa formatada.
        
        Args:
            index: Número da tarefa na lista
            task: Objeto Task
        """
        status_icons = {
            'pendente': '⏳',
            'andamento': '🔄',
            'concluida': '✅'
        }
        priority_icons = {
            'baixa': '🟢',
            'media': '🟡',
            'alta': '🔴'
        }
        
        icon = status_icons.get(task.status, '📌')
        priority = priority_icons.get(task.prioridade, '⚪')
        
        print(f"{index}. {icon} {priority} {task.titulo}")
        if task.descricao:
            print(f"   📝 {task.descricao}")
        if task.tags:
            print(f"   🏷️  {', '.join(task.tags)}")
        if task.data_vencimento:
            print(f"   📅 Vence: {task.data_vencimento}")
        print()


def main():
    """Ponto de entrada principal da aplicação."""
    cli = TaskCrafterCLI()
    cli.run()


if __name__ == '__main__':
    main()
