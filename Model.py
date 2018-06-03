import jsonpickle

class Model:

    def __init__(self):
        self

    className = ""
    classModifiers = []
    extendedClassName = ""
    implementedInterfacesNames = []

    class Field:
        modifiers = []
        isCollection = False
        isPrimitive = False
        typeName = ""
        fieldName = ""

    fields = []

    class Method:
        modifiers = []
        returnType = ""
        isStatic = False
        arguments = []
        name = ""

    methods = []

    class Constructor:
        modifiers = []
        arguments = []

    constructors = []

    def to_json(self):
        jsonpickle.set_encoder_options('simplejson')
        return jsonpickle.encode(self, unpicklable=False)