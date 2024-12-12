import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Optional, List

from app.cli.commands import Command, InitSystemCommand, AddTaskCommand, ShowStatusCommand
from app.distributor.task_distributor import TaskDistributor
from app.node.node import Node


class CLIManager:
    """Singleton class to manage CLI interactions"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.distributor: Optional[TaskDistributor] = None
        self.nodes: List[Node] = []
        self._initialized = True
        self._command_queue = Queue()
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._io_lock = threading.Lock()
    
    def _get_command(self) -> list[str]:
        """Get command from user with synchronized I/O"""
        with self._io_lock:
            try:
                command = input("\nВведите команду (добавить <время>/статус/выход): ").lower().split()
                return command
            except EOFError:
                return ["выход"]
    
    async def _process_command(self, command: list[str]) -> None:
        """Process command and print result with synchronized I/O"""
        try:
            if not command:
                return
                
            if command[0] == "выход":
                with self._io_lock:
                    print("Завершение работы...")
                for node in self.nodes:
                    node.stop()
                return
            
            elif command[0] == "добавить" and len(command) == 2:
                try:
                    duration = int(command[1])
                    if duration <= 0:
                        with self._io_lock:
                            print("Время выполнения должно быть положительным числом")
                        return
                    cmd = AddTaskCommand(self.distributor, duration)
                    result = await cmd.execute()
                    with self._io_lock:
                        print(result)
                except ValueError:
                    with self._io_lock:
                        print("Неверный формат времени выполнения")
            
            elif command[0] == "статус":
                cmd = ShowStatusCommand(self.nodes)
                result = await cmd.execute()
                with self._io_lock:
                    print(result)
            
            else:
                with self._io_lock:
                    print("Неизвестная команда. Доступные команды:")
                    print("  добавить <время> - добавить задание")
                    print("  статус - показать состояние системы")
                    print("  выход - завершить работу")
        
        except Exception as e:
            with self._io_lock:
                print(f"Произошла ошибка: {e}")
    
    def _get_server_count(self) -> int:
        """Get number of servers from user input with validation"""
        while True:
            try:
                num_servers = int(input("Введите количество серверов: "))
                if num_servers <= 0:
                    print("Количество серверов должно быть положительным числом")
                    continue
                return num_servers
            except ValueError:
                print("Пожалуйста, введите корректное число")
    
    async def start(self):
        """Start the CLI interface"""
        with self._io_lock:
            print("Добро пожаловать в симулятор распределенной системы.")
            num_servers = self._get_server_count()
        
        # Инициализация системы
        command = InitSystemCommand(num_servers)
        result = await command.execute()
        self.distributor = command.distributor
        self.nodes = command.nodes
        
        with self._io_lock:
            print(result)

        for node in self.nodes:
            asyncio.create_task(node.run())
        

        while True:
            command = await asyncio.get_event_loop().run_in_executor(
                self._executor, self._get_command
            )
            
            if command and command[0] == "выход":
                await self._process_command(command)
                break
            
            await self._process_command(command)
        
        self._executor.shutdown()