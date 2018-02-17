import csv
import datetime
import os

from peewee import Model, fn

from common.config import serverdb


class BaseModel(Model):

    # @classmethod
    # def update(cls, **update):
    #     update['modified'] = datetime.now()
    #     return super(Model, cls).update(**update)

    @classmethod
    def backup_table(cls, csvfile):
        """
        Create a schema less backup of this model in a csv file.
        """
        query = cls.select()
        if csvfile.tell():
            desc = csvfile.fileno()
            modified = datetime.fromtimestamp(os.path.getmtime(desc))
            query = query.where(cls.modified > modified)
        writer = csv.writer(csvfile)
        writer.writerows(query.naive().tuples())

    @classmethod
    def restore_table(cls, csvfile):
        """
        Restore this model from a csv file.
        """
        latest_id = cls.select(fn.Max(cls.id).alias('latest_id')).scalar()

        # last_id = cls.select(cls.id).

        # reader = csv.reader(csvfile)

        # for row in reader:
        # print(row[0])

    class Meta:
        database = serverdb