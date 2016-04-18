from google.appengine.ext import ndb


class EmailSubscribe(ndb.Model):
    email_addr = ndb.StringProperty(required=True)
    active = ndb.BooleanProperty(required=True)
    sub_content = ndb.StringProperty(repeated=True)


class MailManager(object):

    def __init__(self, email_addr="", sub_content=[]):
        self.email_addr = email_addr
        self.sub_content = sub_content
        return

    def subscribe(self):
        val = EmailSubscribe.query(EmailSubscribe.email_addr == self.email_addr).get()
        if not val:
            EmailSubscribe(email_addr=self.email_addr, active=True,
                           sub_content=self.sub_content).put()
        else:
            if self.sub_content:
                val.sub_content = self.sub_content
            val.active = True

    def unsubscribe(self):
        val = EmailSubscribe.query(EmailSubscribe.email_addr == self.email_addr).get()
        if val:
            val.active = False

    @staticmethod
    def get_subscriber_list(sub_type):
        subscribers = EmailSubscribe.query().fetch()
        l = []
        for subscriber in subscribers:
            if subscriber.active and (sub_type in subscriber.sub_content):
                l.append(subscriber.email_addr)
        return l
