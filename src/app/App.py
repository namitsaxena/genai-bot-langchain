from src.app import AppFactory

if __name__ == "__main__":
    ui = AppFactory.get_app_instance()
    ui.run()
