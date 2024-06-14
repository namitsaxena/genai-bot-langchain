from src.app import AppFactory

if __name__ == "__main__":
    ui = AppFactory.get_app_instance(AppFactory.PROJECT_ID, AppFactory.REGION)
    ui.run()
