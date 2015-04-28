import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertySet;
import com.sun.star.frame.XController;
import com.sun.star.frame.XModel;
import com.sun.star.lang.IllegalArgumentException;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;

static public void snippet(Object oInitialTarget)
{
   try
   {
      XModel xModel = UnoRuntime.queryInterface(
         XModel.class, oInitialTarget);
      XController xController = xModel.getCurrentController();
      
      XPropertySet xPropertySet = UnoRuntime.queryInterface(
         XPropertySet.class, xController);
      int nPageCount = AnyConverter.toInt(xPropertySet.getPropertyValue("PageCount"));
      
   }
   catch (WrappedTargetException e1)
   {
      // getPropertyValue
      e1.printStackTrace();
   }
   catch (IllegalArgumentException e2)
   {
      //
      e2.printStackTrace();
   }
   catch (UnknownPropertyException e3)
   {
      // getPropertyValue
      e3.printStackTrace();
   }
}
