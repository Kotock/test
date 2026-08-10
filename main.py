from parser import WebParser
import logging

logger = logging.getLogger(__name__)

def main():
    print("=" * 50)
    print("ЗАПУСК ПАРСЕРА")
    print("=" * 50)
    
    parser = WebParser()
    
    try:
        data = parser.run(parse_method='quotes')
        
        parser.save_csv()
        parser.save_json()
        
        print("\n" + "=" * 50)
        print("ПАРСИНГ ЗАВЕРШЕН")
        print(f"Всего записей: {len(data)}")
        print("=" * 50)
        
    except KeyboardInterrupt:
        logger.warning("Парсинг прерван пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()