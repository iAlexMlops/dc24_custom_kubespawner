from kubespawner import KubeSpawner
import logging
import ast

from .utils import setup_logger, get_user_groups, load_config, render_template, \
    select_image_from_input


class AlexSpawner(KubeSpawner):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = setup_logger(__name__, logging.ERROR)
        self.logger.info('Start working with AlexSpawner')

        # -------------------------------------
        # Группы, в которые входит пользователь
        # -------------------------------------
        self.user_groups = get_user_groups(self.logger, self.user.name)

        # ---------------------------------------------------
        # !!! Переопределение групп для тестового запуска !!!
        # ---------------------------------------------------
        if self.user.name == 'admin':
            self.user_groups = ['jupyterhub_admins']
        elif self.user.name == 'other_user':
            self.user_groups = ['jupyterhub_other_users']

        # ------------------------------
        # Загружаем конфиг из yaml-файла
        # ------------------------------
        self.groups_data_config = load_config('/tmp/formConf.yaml')

        # -----------------------------------------------------------------------------
        # Идем по списку кандидатов.
        # Если кандидат-группа есть в списке групп пользователя, то выбор падает на нее
        # Если у пользователя нет ниодной группы-кандидата,
        # то ему проставляется группа default
        # -----------------------------------------------------------------------------
        self.group_candidates = ["jupyterhub_admins",
                                 "jupyterhub_other_users"
                                 ]
        self.group_for_render = "default"
        for group in self.group_candidates:
            if group in self.user_groups:
                self.group_for_render = group
                break
        self.form_values = self.groups_data_config['groups'][self.group_for_render]

    def _options_form_default(self):
        # ----------------------------------------------
        # Рендер формы в соответствии с выбраной группой
        # ----------------------------------------------
        form = render_template(self.groups_data_config, self.group_for_render)
        return form

    def options_from_form(self, formdata):
        self.logger.info(f"Formdata: {formdata}")

        # ------------------------------------------------
        # Получение значений с формы из параметра formdata
        # ------------------------------------------------
        image = formdata.get('jupyter_image', [''])[0].strip()
        self.image = select_image_from_input(image)

        cpu = formdata.get('cpu', [''])[0].strip()
        self.cpu_guarantee = round(float(cpu) / 3, 2)
        self.cpu_limit = float(cpu)

        mem = formdata.get('mem', [''])[0].strip()
        self.mem_guarantee = str(mem) + "G"
        self.mem_limit = str(mem) + "G"

        options = {
            'image': self.image,
            'cpu': self.cpu_limit,
            'mem': self.mem_limit,
        }

        return options
