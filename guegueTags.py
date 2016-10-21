try:
    import pymel.core as pmc
except ImportError:
    pass

class GuegueTags(object):
    """wrapper de tags pour guerilla
        wrapper qui genere les tags de base: transform name, top parent name. et 
        possede une serie de methodes permettant d'ajouter ou supprimer des 
        tags guerilla.

        :type obj: transform
        :param obj: object de type transform ou camera ou mesh 
    """

    VALIDE_OBJ = ['camera', 'mesh']
    def __init__(self, obj):
        """ 
        """
        self.obj = obj
        self.group = None
        self.tags = []
        is_valide = self._validity()
        if not is_valide:
            self.obj = None
            raise TypeError("Wrong arg type, must be camera or mesh")
        self._get_top()
        if self.group is None:
            self.tags = [self.obj.name()]
        else:
            self.tags = [self.obj.name(), self.group.name()]
        self._add_exist_tags()
        
    def _validity(self):
        """check si shape ou transform de shape ou transform de cam
        """
        if self.obj.type() == 'transform':
            child = self.obj.getChildren()
            if len(child) == 0:
                child = self.obj
                return False
            else:
                child = child[0]
            if child.type() not in GuegueTags.VALIDE_OBJ:
                return False
            else:
                self.obj = child.getTransform()
                #TODO::remove this pymel fix bug
                if self.obj == None:
                    self.obj = pmc.listRelatives(child, type='transform',p=True)[0]
            return True
        if self.obj.type() in GuegueTags.VALIDE_OBJ:
            self.obj = self.obj.getTransform()
            return True
            
    def _add_exist_tags(self):
        """add all existing guerilla tags to tags list attribute
        """
        try:
            guerilla_tags = self.obj.getAttr("GuerillaTags")
            if guerilla_tags is None:
                return False
            self.tags = self.tags + guerilla_tags.split(',')
        except pmc.MayaAttributeError:
            print "Warning: no guerilla tags present"
        self.tags = filter(None, self.tags)
            
    def _get_top(self):
        """find his topp root group
        """
        if self.obj.getParent() is None:
            self.group = None
        else:
            self.group = self.obj.root()
            
    def add_to_tags(self, tag=None):
        """add extra tag to tags list

            :param tag: extra tag to add must be str
            :type tag: string
        """
        if type(tag) is not str or tag == '':
            raise TypeError("Wrong extra tag type, must be string")
        self.tags.append(tag)
        
    def remove_to_tags(self, tag=None):
        """remove extra tag to tags list

            :type tag: string
            :param tag: tag name to remove
        """
        if type(tag) is not str or tag == '':
            raise TypeError("Wrong tag type to remove, must be string")
        tags_lists = tag.split(',')
        for tag in tags_lists:
            try:
                self.tags.remove(tag)
            except ValueError:
                raise ValueError("{0} is not in object tags".format(tag))
            
    def write_tags(self):
        """write tags in extr attributes object
        """
        self.tags = set(self.tags)
        str_tags = ','.join(self.tags)
        if not pmc.attributeQuery("GuerillaTags", node=self.obj, exists=True):
            pmc.addAttr(self.obj, longName="GuerillaTags", dt="string")
        self.obj.attr("GuerillaTags").set(str_tags)
        
            
# objs = pmc.ls(sl=True)
# for obj in objs:
#     gue = GuegueTags(obj)
#     gue.add_to_tags("metal")
#     gue.tags = []
#     gue.write_tags()
        
