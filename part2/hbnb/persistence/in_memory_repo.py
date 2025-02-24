class InMemoryRepo:
    def __init__(self):
        self.data = {}

    def create(self, model_class, **kwargs):
        if model_class.__name__ not in self.data:
            self.data[model_class.__name__] = {}
        instance = model_class(**kwargs)
        self.data[model_class.__name__][instance.id] = instance
        return instance

    def get(self, model_class, id):
        return self.data.get(model_class.__name__, {}).get(id)

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def delete(self, model_class, id):
        return self.data.get(model_class.__name__, {}).pop(id, None)

    def list(self, model_class):
        return list(self.data.get(model_class.__name__, {}).values())
