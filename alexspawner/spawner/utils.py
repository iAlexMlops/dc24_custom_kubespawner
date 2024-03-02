import yaml
import logging
import os
from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException
from jinja2 import Environment, FileSystemLoader


def load_config(file_path):
    """
    Загрузка конфига из yaml-файла.
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def render_template(config, group):
    """
    Рендеринг шаблона формы.
    :param config:
    :param group:
    :return:
    """
    template_path = os.path.join(os.path.dirname(__file__), '../templates')
    template_loader = FileSystemLoader(searchpath=template_path)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template("form.html.jinja2")

    rendered_code = template.render(config=config['groups'], someGroup=group)

    return rendered_code


def setup_logger(logger_name, level=logging.INFO):
    """
    Настройка логгера в консоль.
    :param logger_name:
    :param level:
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def select_image_from_input(image):
    """
    Возвращает имя образа из переменных окружения.
    :param image:
    :return:
    """
    docker_registry = os.environ.get('DOCKER_REGISTRY')
    docker_tag = os.environ.get('DOCKER_TAG')
    return f"{docker_registry}/{image}:{docker_tag}"


def get_user_groups(logger, username) -> list:
    """
    Возвращает список групп, в которых состоит пользователь.
    Проверяются все группы и идет сравнение всех пользователей с именем настоящего.

    :rtype: object
    """
    ldap_server = os.environ.get('ALEX_SPAWNER_LDAP_SERVER')
    ldap_user = os.environ.get('ALEX_SPAWNER_LDAP_USER')
    ldap_password = os.environ.get('ALEX_SPAWNER_LDAP_PASSWORD')
    base_dn = os.environ.get('ALEX_SPAWNER_LDAP_BASE_DN')

    try:
        server = Server(ldap_server, get_info=ALL)
        connection = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)

        # Поиск пользователя в LDAP по его имени
        user_filter = '(&(objectClass=user)({}={}))'.format('sAMAccountName', username)
        connection.search(search_base=base_dn, search_filter=user_filter, search_scope=SUBTREE,
                          attributes=['memberOf'])

        if not connection.entries:
            print("Пользователь не найден.")
            return []

        # Получение групп, к которым принадлежит пользователь
        groups = [group.split(',')[0][3:] for group in connection.entries[0].memberOf.values]
        logger.info(f"Found {format(len(groups))} groups for user {username}")
        logger.debug(f"Groups:")
        for group in groups:
            logger.debug(f"\t{group}")

        connection.unbind()

        return groups

    except LDAPException as e:
        logger.error(f"LDAP Error: \n{e}")
        return []
