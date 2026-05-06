# Monkey-patch Django to support MariaDB 10.4.x (XAMPP default)
try:
    import django.db.backends.base.base as base_base
    base_base.BaseDatabaseWrapper.check_database_version_supported = lambda self: None
    
    import django.db.backends.mysql.features as mysql_features
    mysql_features.DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
    mysql_features.DatabaseFeatures.can_return_rows_from_bulk_insert = property(lambda self: False)
except ImportError:
    pass

