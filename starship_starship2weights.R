#################################
## DATA MINING - MTAT.03.183
## 5. JAN 2018
## MÄRTEN VESKIMÄE
#################################

library(tidyverse)
library(data.table)

load("starship_data.Rda")
load("tln_roads.Rda")

tallinn_nodes = tln_roads$nodes$attrs[c("lon","lat")]
tallinn_nodes = tallinn_nodes[!duplicated(tallinn_nodes),]

find_nearest_node = function(lon_ss,lat_ss){
  box = tallinn_nodes[tallinn_nodes$lon > (lon_ss-0.001) &
                      tallinn_nodes$lon < (lon_ss+0.001) &
                      tallinn_nodes$lat > (lat_ss-0.001) &
                      tallinn_nodes$lat < (lat_ss+0.001),]
  if(nrow(box)>0){
    box$dist = (lon_ss-box$lon)^2 + (lat_ss-box$lat)^2
    box[box$dist==min(box$dist),][1,1:2]
  } else data.frame(lat = NA, lon = NA)
}

road_quality = starship_data %>% filter(standstill_detected!=1)

nearest_nodes = lapply(1:nrow(road_quality),function(i){
  find_nearest_node(road_quality$coordinates_long[i],road_quality$coordinates_lat[i])
  })
nearest_nodes = data.frame(rbindlist(nearest_nodes))

road_quality$lon = nearest_nodes$lon
road_quality$lat = nearest_nodes$lat

road_quality_new =  road_quality %>%
  group_by(lon,lat) %>%
  summarise(quality = (
    ((var(orientation_delta_z,na.rm=T)+1)*
      (var(starship_data$accel_vec_z,na.rm=T)+1))
    ^10000)/100000) %>%
  na.omit()
x <- road_quality_new$quality
x <- (x-min(x))/(max(x)-min(x))
road_quality_new$quality <- x

road_quality %>%
  ggplot() +
  geom_point(data=tallinn_nodes, aes(lon,lat),alpha=.1,size=.02) +
  geom_point(aes(lon,lat,color=quality)) +
  theme_void()+
  scale_color_gradient(low="yellow",high="red")

save(road_quality_new,file="road_quality.Rda")
