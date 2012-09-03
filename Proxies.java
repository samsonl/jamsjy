import java.lang.reflect.*;
import javax.jms.ConnectionFactory;
import javax.jms.Connection;
import javax.jms.Session;
import javax.jms.TextMessage;
import javax.jms.MessageProducer;
import javax.jms.Queue;
import javax.jms.MessageConsumer;
import javax.jms.JMSException;

import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;
import org.python.core.PySystemState;
import org.python.core.PyInstance;

class BaseConnectionFactory implements ConnectionFactory {
    public Connection createConnection(String userName, String passord) throws JMSException {
        //PythonInterpreter interpreter = new PythonInterpreter();
        PythonInterpreter interpreter = new PythonInterpreter(null, new  PySystemState());

        interpreter.exec("from server import BaseConnectionFactory");

        PyObject cf = interpreter.get("BaseConnectionFactory");
        PyObject cfo = cf.__call__();

        ConnectionFactory cfj = (ConnectionFactory)cfo.__tojava__(ConnectionFactory.class);
        Connection con = null;
        try {
          con = cfj.createConnection();
        } catch (JMSException e) { 
          throw e;
        }
        return con;
    }

    public Connection createConnection() throws JMSException {
        return createConnection(null, null);
    }

}



public class Proxies {

  public static void main(String [] args) {



    try { 
      Connection c = new BaseConnectionFactory().createConnection();

      System.out.println(c.getMetaData().getJMSProviderName());

      Session sess = c.createSession(false, Session.AUTO_ACKNOWLEDGE );

      Queue q = sess.createQueue("AAAa");
      MessageProducer pub = sess.createProducer(q);
      MessageConsumer sub = sess.createConsumer(q);
      c.start();

      TextMessage tm = sess.createTextMessage();
      tm.setText("OK1");
      pub.send(q,tm);

      tm = sess.createTextMessage();
      tm.setText("OK2");
      pub.send(q,tm);

      TextMessage messRec = (TextMessage)sub.receiveNoWait();
      System.out.println(messRec.getText());
      messRec = (TextMessage)sub.receiveNoWait();
      System.out.println(messRec.getText());

      messRec = (TextMessage)sub.receiveNoWait();
      System.out.println(messRec);

    } catch (JMSException e) {
      e.printStackTrace();
    }

  }
}

