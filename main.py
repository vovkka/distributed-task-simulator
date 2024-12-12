import asyncio
import logging
from app.cli.cli_manager import CLIManager


async def main():
    """Main entry point of the distributed system simulator"""
    try:
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        cli_manager = CLIManager()
        await cli_manager.start()
    
    except KeyboardInterrupt:
        logging.info("Получен сигнал завершения работы")
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        logging.error(e.__traceback__)
        raise
    finally:
        logging.info("Завершение работы системы")


if __name__ == '__main__':
    asyncio.run(main())
