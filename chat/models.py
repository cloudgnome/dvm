from django.db.models import Model,CharField,ForeignKey,BooleanField,DateTimeField,CASCADE
from user.models import User

class Chat(Model):
    sender = ForeignKey(User,on_delete=CASCADE)
    reciever = ForeignKey(User,on_delete=CASCADE,related_name="messages")
    is_read = BooleanField(default=0)
    time = DateTimeField(auto_now_add=True)

    @property
    def last_message(self):
        return self.messages.last().text

    @property
    def name(self):
        return self.sender.full_name

    @property
    def list(self):
        return [item.dict() for item in self.messages.all()]

    class Meta:
        unique_together = ['sender','reciever']
        ordering = ['-time']

class Message(Model):
    text = CharField(max_length=255)
    owner = ForeignKey(User,related_name='sent_messages',on_delete=CASCADE,null=True)
    chat = ForeignKey(Chat,related_name='messages',on_delete=CASCADE)

    def dict(self):
        return {'text':self.text,'owner':self.owner.id}