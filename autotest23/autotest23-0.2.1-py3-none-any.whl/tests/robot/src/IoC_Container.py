"""
An unintrusive library for dependency injection in modern Python. 
Inspired by Funq, Punq is a dependency injection library you can understand.
https://punq.readthedocs.io/en/latest/
"""
import punq
#-------------------------------------------------------------------------------
from .autolocatormanager.src.abstract.i_scraper import IScraper
from .autolocatormanager.src.scraping import Scraping
from .autolocatormanager.src.abstract.i_auto_nav_locator_handler import IAutoNavLocatorHandler
from .autolocatormanager.src.auto_nav_locator_handler import AutoNavLocatorHandler
from .autolocatormanager.src.abstract.i_module_locator_writer import IModuleLocatorWriter
from .autolocatormanager.src.module_locator_writer import ModuleLocatorWriter
from .autolocatormanager.src.abstract.i_user_hander import IUserHandler
from .autolocatormanager.src.user_handler import UserHandler
from .autolocatormanager.src.abstract.i_scrap_page_by_nav_route import IScrapPageByNavRoute
from .autolocatormanager.src.scrap_page_by_nav_route import ScrapPageByNavRoute
#-------------------------------------------------------------------------------
from .passwordmanager.constants import *
from .passwordmanager.src.abstract.i_security_key import ISecurityKey
from .passwordmanager.src.key_generator import KeyManager
from .passwordmanager.src.abstract.i_user_credentials import IUserCredentials
from .passwordmanager.src.user_credentials import UserCredentials
#-------------------------------------------------------------------------------
from .managepom.src.abstract.i_pom_abstract_factory import IPOMAbstractFactory
from .managepom.src.abstract.i_module_generator import IModuleGenerator
from .managepom.src.abstract.i_pom_module_handler import IPOMModuleHandler
from .managepom.src.abstract.i_pom_structure import IPOMStructure
from .managepom.src.abstract.i_automation import IAutomation
#-------------------------------------------------------------------------------
from .managepom.src.package_manager import PackageManager
from .managepom.src.package_handler import PackageHandler
from .managepom.src.module_generator import ModuleGenerator
from .managepom.src.module_handler import ModuleHandler
from .managepom.src.automation_module_generator import AutomationModuleGenerator


CONTAINER = punq.Container()
print("Initializing IoC Container......")
# Regiser 
#-------------------------------------------------------------------------------
CONTAINER.register(ISecurityKey, KeyManager)
user_cred_instance = UserCredentials(USER_CREDENTIALS_FILE_PATH, KEY_FILE_PATH, ISecurityKey) # Dependency Injection
CONTAINER.register(IUserCredentials, instance= user_cred_instance)
#-------------------------------------------------------------------------------
CONTAINER.register(IPOMAbstractFactory, PackageManager)
CONTAINER.register(IPOMStructure, PackageHandler)
module_handler_instance = ModuleHandler(IPOMStructure)  # Dependency Injection
CONTAINER.register(IPOMModuleHandler, instance= module_handler_instance)
module_generator_instance = ModuleGenerator(IPOMModuleHandler)  # Dependency Injection
CONTAINER.register(IModuleGenerator, instance= module_generator_instance)
CONTAINER.register(IAutomation, AutomationModuleGenerator)
#-------------------------------------------------------------------------------
CONTAINER.register(IScraper, Scraping)
CONTAINER.register(IAutoNavLocatorHandler, AutoNavLocatorHandler)
scraper_obj = CONTAINER.resolve(IScraper)
scraper_page_by_nav_route_obj = ScrapPageByNavRoute(scraper_obj) # Dependency Injection
CONTAINER.register(IScrapPageByNavRoute, instance= scraper_page_by_nav_route_obj) 
CONTAINER.register(IModuleLocatorWriter, ModuleLocatorWriter)
CONTAINER.register(IUserHandler, UserHandler)
