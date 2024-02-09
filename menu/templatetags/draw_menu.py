from django import template

from menu.models import MenuPage

register = template.Library()


class MenuItem:
    instances = []

    def __init__(self, page_id, url, parent_id, order, title, title_in_menu):
        self.page_id = page_id
        self.url = url
        self.order = order
        self.parent_id = parent_id
        self.title = title
        self.title_in_menu = title_in_menu
        self.children = []
        self.is_active = False
        self.is_opened = False
        MenuItem.instances.append(self)

    @classmethod
    def get(cls, page_id):
        return [instance for instance in cls.instances
                if instance.page_id == page_id]

    def open_menu_items(self):
        self.open_parents()
        self.open_before_items()

    def open_parents(self):
        root_parent = self.get_root_item()
        if self != root_parent:
            root_parent.open_children(stop_item=self)
        root_parent.is_opened = True

    def get_root_item(self):
        root_item = None
        temp_id = self.parent_id
        while temp_id:
            parent_instance = MenuItem.get(page_id=temp_id)[0]
            temp_id = parent_instance.parent_id
            root_item = parent_instance
        return root_item if root_item else self

    def open_before_items(self):
        root_item = self.get_root_item()
        before_root_items = []
        for instance in MenuItem.instances:
            if instance.order < root_item.order and not instance.parent_id:
                before_root_items.append(instance)
        for item in before_root_items:
            item.is_opened = True
            item.open_children()

    def open_children(self, stop_item=None):
        for child in self.children:
            if child == stop_item:
                child.is_opened = True
                break
            child.is_opened = True
            child.open_children(stop_item)

    def set_children(self):
        if self.parent_id:
            parent_instances = MenuItem.get(page_id=self.parent_id)
            for parent_inst in parent_instances:
                parent_inst.children.append(self)


@register.inclusion_tag(filename='menu/menu_template_first_level.html',
                        takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].get_full_path()
    menu = (MenuPage.objects
            .select_related()
            .filter(menu=menu_name).order_by('parent', 'order'))
    menu_items = []
    current_menu_item = None
    for item in menu:
        menu_item_instance = MenuItem(
            item.page_id,
            item.page.get_absolute_url(),
            item.parent_id,
            item.order,
            item.page.title,
            item.page.title_in_menu
        )

        if current_url == menu_item_instance.url:
            menu_item_instance.is_active = True
            current_menu_item = menu_item_instance

        menu_item_instance.set_children()
        menu_items.append(menu_item_instance)

    if current_menu_item:
        current_menu_item.open_menu_items()
    MenuItem.instances.clear()

    return {'menu': menu_items}
