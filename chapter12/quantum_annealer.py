import  time 
import  math 
import  numpy  as  np 
import  os 
import  random 

import json
import argparse




def  distance ( point1 ,  point2 ): 
    return  math.sqrt (( point1 [ 1 ] - point2 [ 1 ]) ** 2  +  ( point1 [ 0 ] - point2 [ 0 ]) ** 2 )


def  calcuatetSpinConfiguration():

    def  Spin_config_at_a_time_in_a_TROTTER_DIM ( tag ): 
        config  =  list ( - np.ones ( NCITY ,  dtype  =  np.int )) 
        config [ tag ]  =  1 
        return  config

    def  Spin_config_in_a_TROTTER_DIM ( Tag ): 
        spin  =  [] 
        spin.append( Config_at_init_time ) 
        for  i  in  range ( TOTAL_TIME - 1 ): 
            spin.append(list( Spin_config_at_a_time_in_a_TROTTER_DIM ( Tag[i])) ) 
        return  spin

    Spin  =  [] 
    for  i  in  range ( TROTTER_DIM ): 
        Tag  =  np.arange(1,NCITY ) 
        np.random.shuffle( Tag )
        Spin.append( Spin_config_in_a_TROTTER_DIM ( Tag ))  
    return  Spin


def  calculateShortestRoute ( Config,max_distance ):    
    Length  =  [] 
    for  i  in  range ( TROTTER_DIM ): 
        Route  =  [] 
        for  j  in  range ( TOTAL_TIME ): 
            Route.append ( Config [ i ] [ j ] . index ( 1 )) 
        Length.append ( calculateTotaldistance ( Route,max_distance ))

    min_Tro_dim  =  np . argmin ( Length ) 
    Best_Route  =  [] 
    for  i  in  range ( TOTAL_TIME ): 
        Best_Route.append ( Config [ min_Tro_dim ] [ i ] . index ( 1 )) 
    return  Best_Route


def  calculateTotaldistance ( route, max_distance): 
    Total_distance  =  0 
    for  i  in  range(TOTAL_TIME): 
        Total_distance  +=  distance(POINT[route[i]], POINT[route[( i + 1) % TOTAL_TIME]])/max_distance
    return  Total_distance


def  calculateRealTotaldistance ( Route ): 
    Total_distance  =  0 
    for  i  in  range(TOTAL_TIME): 
        Total_distance  +=  distance(POINT [ Route [ i ]],  POINT[Route[( i + 1 ) % TOTAL_TIME]] ) 
    return  Total_distance

def  calculateRealdistance ( Route ): 
    Total_distance  =  0 
    for  i  in  range(len(Route)): 
        if i < len(Route)-1:
           Total_distance  +=  distance(POINT [ Route [ i ]],  POINT[Route[( i + 1 )]] ) 
    return  Total_distance

def   moveQuantumMonteCarlo( config ,  Ann_para ): 
    c  =  np.random.randint ( 0 , TROTTER_DIM ) 
    a_  =  list(range(1,TOTAL_TIME ))
    a  =  np.random.choice ( a_ ) 
    a_.remove( a ) 
    b  =  np.random.choice (a_ )

    p  =  config [c][a].index(1)
    q  =  config [c][b].index(1)

    delta_cost  =  delta_costc  =  delta_costq_1  =  delta_costq_2  =  delta_costq_3  =  delta_costq_4  =  0

    for  j  in  range ( NCITY ): 
        l_p_j  =  distance (POINT [p],  POINT [j]) / max_distance 
        l_q_j  =  distance (POINT [q],  POINT [j]) / max_distance 
        delta_costc  +=  2*(- l_p_j * config[c][a][p] - l_q_j * config[c][a][q]) * (config[c][a-1][j] + config[c][(a+1)%TOTAL_TIME][j]) + 2*(-l_p_j * config[c][b][p] - l_q_j*config[c][b][q])*(config[c][b-1][j]+config[c][(b+1)%TOTAL_TIME][j])

        
    para  =  ( 1 / BETA ) * math.log( math.cosh ( BETA * Ann_para / TROTTER_DIM ) / math.sinh ( BETA * Ann_para / TROTTER_DIM )) 
    delta_costq_1  =  config [ c ] [ a ] [ p ] * ( config [( c - 1 )% TROTTER_DIM ] [ a ] [ p ] + config [( c + 1 ) % TROTTER_DIM ] [ a ] [ p ]) 
    delta_costq_2  =  config [ c ] [ a ] [ q ] * ( config [( c - 1 ) % TROTTER_DIM] [ a ] [ q ] + config [( c + 1 ) % TROTTER_DIM] [ a ] [ q ]) 
    delta_costq_3  =  config [ c ] [ b ] [ p ] * ( config [( c - 1 ) % TROTTER_DIM ] [ b ] [ p ] + config [( c + 1 ) % TROTTER_DIM ] [ b ] [ p ]) 
    delta_costq_4  =  config [ c ] [ b ] [ q ] *( config [( c - 1 ) % TROTTER_DIM ] [ b ] [ q ] + config [( c + 1 ) % TROTTER_DIM ] [ b ] [ q ])

    delta_cost  =  delta_costc / TROTTER_DIM + para * ( delta_costq_1 + delta_costq_2 + delta_costq_3 + delta_costq_4 )

    if  delta_cost  <=  0 : 
        config [ c ] [ a ] [ p ] *= -1 
        config [ c ] [ a ] [ q ] *= -1 
        config [ c ] [ b ] [ p ] *= -1 
        config [ c ] [ b ] [ q ] *= -1 
    elif  np . random . random ()  < np . exp ( - BETA * delta_cost ): 
        config [ c ] [ a ] [ p ] *= - 1 
        config [ c ] [ a ] [ q ] *= - 1 
        config [ c ] [ b ] [ p ] *= - 1 
        config [ c ] [ b ] [ q ] *= - 1

    return  config

def   verifyRouteConfiguration(routes,pick_deliveries):
      for i in range(len(routes)):
          route = routes[i]
          for j in range(len(route)):
              route_index = route[j]
              #print(route_index)
              for k in range(len(pick_deliveries)):
                  pick_delivery = pick_deliveries[k] 
                  pick = pick_delivery["pickup"]
                  delivery = pick_delivery["delivery"]
                  if route_index == delivery and route_index !=0:
                     check = verifyPick(pick,delivery,route) 
                     if not check:
                        return False
                   
                         
      return True                    
def  verifyPick(pick_index,delivery_index, route):
     picked = False
     delivery_passed = False
    
     for i in range(len(route)):
         route_i = route[i]    
         if pick_index == route_i: 
            picked = True
         if delivery_index == route_i and picked:
            return True
     return False    

 
if  __name__  ==  '__main__' :
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputs", type=argparse.FileType('r'),
                    help="inputs as a json file")
    parser.add_argument("-d", "--distances", type=argparse.FileType('r'),
                    help="distances as a json file")
    parser.add_argument("-t", "--trucks", type=argparse.FileType('r'),
                    help="trucks as a json file")
    parser.add_argument("-p", "--pickups", type=argparse.FileType('r'),
                    help="pickups as a json file")

    args = parser.parse_args()

    REDUC_PARA  =  0.99

    inputs = json.load(args.inputs)
    distances = json.load(args.distances)
    trucks = json.load(args.trucks)
    pickup_deliveries = json.load(args.pickups)


    TROTTER_DIM  =  int ( inputs["trotter_dimension"]) 
    ANN_PARA  =   float ( inputs["initial_annealing"]) 
    ANN_STEP  =  int ( inputs["annealing_step"]) 
    MC_STEP  =  int ( inputs["montecarlo_step"]) 
    BETA  =  float ( inputs["inverse_temperature"]) 
 
    NCITY  =  len( distances )
    POINT  =  [[0]*2]*NCITY
    TOTAL_TIME  =  NCITY 
    
    num_trucks = len(trucks)

    for  i  in  range ( NCITY ):
         distance_node = distances.pop()

         node = [0]*2
         node[0] = float(distance_node["x"])
         node[1] = float(distance_node["y"])
 
         POINT [NCITY-1-i]  =  node

    max_distance  =  0 
    for  i  in  range ( NCITY ): 
        for  j  in  range ( NCITY ): 
            node_distance = distance ( POINT [ i ],  POINT [ j ])
            if  max_distance  <=  distance ( POINT [ i ],  POINT [ j ]): 
                max_distance  =  distance ( POINT [ i ],  POINT [ j ])

    Config_at_init_time  =  list( -np.ones( NCITY,dtype = np.int )) 
    Config_at_init_time [ 0 ]  =  1

    print("starting the annealing process ...")
    t0  =  time.clock ()

    np.random.seed(100) 
    spin  =  calcuatetSpinConfiguration () 
    LengthList  =  [] 
    truck_routes = []
    check = False
    for  t  in  range ( ANN_STEP ): 
        for  i  in  range ( MC_STEP ): 
            con  =  moveQuantumMonteCarlo( spin ,  ANN_PARA ) 
            rou  =  calculateShortestRoute( con,max_distance ) 
            length  =  calculateRealTotaldistance ( rou ) 
            nprou = np.array(rou)
            truck_routes = np.split(nprou,num_trucks)
            check = verifyRouteConfiguration(truck_routes,pickup_deliveries)  
        LengthList .append ( length ) 
        print("No: Step: {}, Annealing process Parameter: {}" . format ( t + 1 , ANN_PARA )) 
        ANN_PARA  *=  REDUC_PARA
    check = verifyRouteConfiguration(truck_routes,pickup_deliveries)    
    if check:
        truck = 0;        
        for route in truck_routes:
            route_distance = calculateRealdistance(route)
            print("Route for truck",truck," ",route, "distance ",route_distance)
            truck = truck +1    
    Route  =  calculateShortestRoute( spin,max_distance ) 
    Total_Length  =  calculateRealdistance ( Route ) 
    Elapsed_time  =  time.clock () - t0

    print("SHORTEST ROUTE : {}" . format ( Route ) )
    print("SHORTEST DISTANCE: {}" . format ( Total_Length )) 
    print("PROCESSING TIME: s {}" . format ( Elapsed_time ))

