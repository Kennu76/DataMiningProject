#library(RJSONIO)
#library(dplyr)
#library(data.table)
processFile = function(filepath) {
  sensors = list()
  new_row = list()
  i = 0
  j = 0
  con = file(filepath, "r")
  while(T){
    i = i+1
    # if(i > 1000) break
    if(i%%10000==0) print(i)
    line = readLines(con,n=1)
    if(length(line)==0) break
    line = fromJSON(line)
    meta = line$meta %>% as.data.frame()
 #   if(meta$botid %in% bots){
      j = j + 1
      orientation_delta = t(as.data.frame(line$data$orientation_delta))
      colnames(orientation_delta) = c("orientation_delta_x","orientation_delta_y","orientation_delta_z","orientation_delta_w")
      accel_vec = t(as.data.frame(line$data$accel_vec))
      colnames(accel_vec) = c("accel_vec_x","accel_vec_y","accel_vec_z")
      other = as.data.frame(line$data[4:11])
      new_row[[j]] = cbind(meta,orientation_delta,accel_vec,other)
#    }
  }
  close(con)
  data.frame(rbindlist(new_row))
}

#read file in
filepath = "C:/Users/Kevin/Desktop/Datamining/Project/DataMiningProject/starship/example_sensor_data.json"
new_file = processFile(filepath)

new_file <- new_file[-c(1, 2, 3,4), ]
#library(ggplot2)
# Basic line plot with points
orientation_x = ggplot(data=new_file, aes(y=orientation_delta_z, x=secs, group=1)) +
  geom_line()+
  geom_point()


accel_x = ggplot(data=new_file, aes(y=accel_vec_z, x=secs, group=1)) +
  geom_line()+
  geom_point()


numbers_data <- subset(new_file,select = orientation_delta_x:accel_vec_z)

numbers_data$orientation_delta_w<-NULL

pca <- prcomp(numbers_data)

comp <- data.frame(pca$x[,2:3])
# Plot
plot(comp, pch=16, col=rgb(0,0,0,0.5))



test1 <- c(1,2,3,4,5)
test2 <- c(0,1,2,3,4)
plot((new_file$orientation_delta_x-new_file$accel_vec_z)*1000)

snip_of_data1 <- new_file$orientation_delta_z[1:10]
snip_of_data2 <- new_file$orientation_delta_z[10:20]
sd(snip_of_data1)*1000000000
sd(snip_of_data2)*1000000000

sds <- c()
secs <- c()
i = 0
for(m in 1:(length(new_file$orientation_delta_z)/28)){
  print(m)
  secs <- (new_file$orientation_delta_z[((m-1)*28+1):(m*28)])-(new_file$accel_vec_z[((m-1)*28+1):(m*28)])
  sds<-c(sds,sd(secs))
}