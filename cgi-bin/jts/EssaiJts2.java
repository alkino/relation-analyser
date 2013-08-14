import com.vividsolutions.jts.geom.*;
import com.vividsolutions.jts.io.WKTReader;
import java.util.*;

public class EssaiJts
{   
   public static void main(String[] args)
     throws Exception
     {
		
	// read a geometry from a WKT string (using the default geometry factory)
	//Geometry g1 = new WKTReader().read("LINESTRING (0 0, 10 10, 20 20)");
	//System.out.println("Geometry 1: " + g1);
	
	// create a geometry by specifying the coordinates directly
	//Coordinate[] coordinates = new Coordinate[]{new Coordinate(0, 0),
	//   new Coordinate(10, 10), new Coordinate(20, 20)};
	
	// use the default factory, which gives full double-precision
	//Geometry g2 = new GeometryFactory().createLineString(coordinates);
	//System.out.println("Geometry 2: " + g2);
	
	// compute the intersection of the two geometries
	//Geometry g3 = g1.intersection(g2);
	//System.out.println("G1 intersection G2: " + g3);
	
	// from args
	//Geometry g4 = new WKTReader().read(args[0]);
	//System.out.println("Geometry 4: " + g4);
	
	WKTReader rdr = new WKTReader();
	LineString line1 = (LineString) (rdr.read(args[0]));
	showSelfIntersections(line1);
	
     }
   
   
   public static void showSelfIntersections(LineString line) {	
      //System.out.println("Line: " + line);
      //System.out.println("Self Intersections: " + lineStringSelfIntersections(line));
      System.out.println(lineStringSelfIntersections(line));
   }
   
   public static Geometry lineStringSelfIntersections(LineString line) {
      Geometry lineEndPts = getEndPoints(line);
      Geometry nodedLine = line.union(lineEndPts);
      Geometry nodedEndPts = getEndPoints(nodedLine);
      Geometry selfIntersections = nodedEndPts.difference(lineEndPts);
      return selfIntersections;
   }
   
   
   public static Geometry getEndPoints(Geometry g) {	
      List endPtList = new ArrayList();
      if (g instanceof LineString) {
	 LineString line = (LineString) g;
	 endPtList.add(line.getCoordinateN(0));
	 endPtList.add(line.getCoordinateN(line.getNumPoints() - 1));
      }
      else if (g instanceof MultiLineString) {
	 MultiLineString mls = (MultiLineString) g;
	 for (int i = 0; i < mls.getNumGeometries(); i++) {
	    LineString line = (LineString) mls.getGeometryN(i);
	    endPtList.add(line.getCoordinateN(0));
	    endPtList.add(line.getCoordinateN(line.getNumPoints() - 1));
	 }	 
      }
      Coordinate[] endPts = CoordinateArrays.toCoordinateArray(endPtList);
      return (new GeometryFactory()).createMultiPoint(endPts);
   }
   
}
