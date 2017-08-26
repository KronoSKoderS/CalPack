from calpack import models

num_words = 13

class Pkt(models.Packet):
    _word_size = 16
    field1 = models.IntField()
    field2 = models.IntField(little_endian=True)
    field3 = models.IntField(little_endian=True)
    field4 = models.IntField(bit_len=14)
    field5 = models.IntField(bit_len=2)
    field6 = models.IntField(num_words=num_words)
    field7 = models.IntField(num_words=num_words)

    

p = Pkt()

p.field1 = 2
p.field2 = 2
p.field1 == p.field2

p2 = Pkt(field1=1, field2=2, field6=range(num_words))