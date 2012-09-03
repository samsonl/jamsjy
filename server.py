a = 2
if a == 2:
 import sys.path as path
 path.append("jms1.1\lib\jms.jar")

# Notes:
#   Ports
#   jython code as message


from javax.jms import ConnectionFactory
from javax.jms import Connection
from javax.jms import ConnectionMetaData
from javax.jms import Session
from javax.jms import Queue
from javax.jms import MessageProducer
from javax.jms import MessageConsumer
from javax.jms import TextMessage


class BaseMessagePort:
  def __init__(self, portName):
    self.portName = portName
    
  def addMessage(self, message):
    pass
  def removeMessage(self):
    return None
    
  

class BaseMessageStore:
  def __init__(self):
    self.store = {}
  def put(self, dest, msg):
    if not dest in self.store:
      self.store[dest] = []
    self.store[dest].append(msg)
  def get(self, dest):
    return self.store[dest].pop(0)
  def messageCount(self, dest):
    return len(self.store[dest])

class BaseMessageConsumer(MessageConsumer):
  def __init__(self, dest, ms):
    self.ms = ms
    self.dest = dest
  def receiveNoWait(self):
    if self.ms.messageCount(self.dest.getQueueName()) == 0:
      return None
    return self.ms.get(self.dest.getQueueName())

class BaseMessageProducer(MessageProducer):
  def __init__(self, ms):
    self.ms = ms
  def send(self, dest, message):
    self.ms.put(dest.getQueueName(),message)

class BaseQueue(Queue):
  def __init__(self, name):
    self.name = name
  def getQueueName(self):
    return self.name
  
class BaseTextMessage(TextMessage):
  def getText(self):
    return self.textv
  def setText(self, textp):
    self.textv = textp

class BaseSession(Session):
  def __init__(self):
    self.messageStore = BaseMessageStore()

  def close(self):
    nop
  def commit(self):
    nop
  def createBrowser(self, queue):
    nop
  def createBrowser(self, queue, messageSelector):
    nop
  def createBytesMessage(self):
    nop
  # createConsumer(self, destination):
  # createConsumer(self, destination, messageSelector):
  # createConsumer(self, destination, messageSelector, NoLocal):
  def createConsumer(self, *args):
    return BaseMessageConsumer(args[0],self.messageStore)
  def createDurableSubscriber(self, topic, name):
    nop
  def createDurableSubscriber(self, topic, name, messageSelector, noLocal):
    nop
  def createMapMessage(self):
    nop
  def createMessage(self):
    nop
  def createObjectMessage(self):
    nop
  def createObjectMessage(self, object):
    nop
  def createProducer(self,destination):
    return BaseMessageProducer(self.messageStore)
  def createQueue(self,queueName):
    return BaseQueue(queueName)
  def createStreamMessage(self):
    nop
  def createTemporaryQueue(self):
    nop
  def createTemporaryTopic(self):
    nop
  # createTextMessage(self, text):
  # createTextMessage(self):
  def createTextMessage(self, *args):
    return BaseTextMessage()
  def createTopic(self,topicName):
    nop
  def getAcknowledgeMode(self):
    nop
  def getMessageListener(self):
    nop
  def getTransacted(self):
    nop
  def recover(self):
    nop
  def rollback(self):
    nop
  def run(self):
    nop
  def setMessageListener(self, listener):
    nop
  def unsubscribe(self, name):
    nop

class BaseConnectionMetaData(ConnectionMetaData): 
  def getJMSMajorVersion(self):
    return 1
  def getJMSMinorVersion(self):
    return 1
  def getJMSProviderName(self):
    return "Jamjy"
  def getJMSVersion(self):
    return "1.1"
  def getJMSXPropertyNames(self):
    return None
  def getProviderMajorVersion(self):
    return 1
  def getProviderMinorVersion(self):
    return 0
  def getProviderVersion(self):
    return "1.0"


class BaseConnection(Connection): 
  def __init__(self):
    self.metadata = BaseConnectionMetaData()
  def close(self):
    nop
  def createConnectionConsumer(self,destination, messageSelector, sessionPool, maxMessages):
    nop
  def createDurableConnectionConsumer(self,topic, subscriptionName, messageSelector, sessionPool, maxMessages):
    nop
  def createSession(self,transacted, acknowledgeMode):
    return BaseSession()
  def getClientID(self,):
    return self.clientID
  def getExceptionListener(self,):
    nop
  def getMetaData(self):
    return self.metadata
  def setClientID(self,clientID):
    self.clientID = clientID
  def setExceptionListener(self,listener):
    nop
  def start(self):
    self.started = True
  def stop(self):
    self.started = False


class BaseConnectionFactory(ConnectionFactory): 
  # createConnection(self):
  # createConnection(self,userName, password):
  def createConnection(self,*args):
    print "jython connection created"
    return BaseConnection()

########################################################################


if a == 2:
  cf = BaseConnectionFactory()
  ##conn = cf.createConnection()
  conn = cf.createConnection("fred","nurks")
  print conn.getMetaData().getJMSProviderName()
 
  sess = conn.createSession(False, Session.AUTO_ACKNOWLEDGE )
  tm = sess.createTextMessage()
  tm.setText("OK")

  q = sess.createQueue("AAA")
  pub = sess.createProducer(q);
  sub = sess.createConsumer(q);
  conn.start()
  pub.send(q,tm)
  messRec = sub.receiveNoWait()
  print messRec.getText()


