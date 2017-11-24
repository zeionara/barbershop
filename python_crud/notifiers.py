def notify(operation, ident):
    print("%s item with id %i" % (operation, ident))

def notify_insert(ident):
    notify("Inserted",ident)

def notify_delete(ident):
    notify("Deleted",ident)

def notify_update(ident):
    notify("Updated",ident)
