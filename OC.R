library(ncdf4)
library(raster)
## Reading netcdf file
nc <- nc_open('C:\\Users\\lxiao\\Desktop\\20201019\\SST20170505T190011.nc')
out <- "C:\\Users\\lxiao\\Desktop\\20201019\\SST20170505T190011_R.tif"
CRS <- "C:\\Users\\lxiao\\Desktop\\20201019\\CRS.txt"
v <- nc$var[[1]]
size <- v$varsize
dims <- v$ndims
nt <- size[dims]              # length of time dimension

lat <- nc$var$`navigation_data/latitude`
lon <- nc$var$`navigation_data/longitude`

# read sst variable
r<-list()
for (i in 1:nt) {
    start <- rep(1,dims)     # begin with start=(1,1,...,1)
    start[dims] <- i             # change to start=(1,1,...,i) to read    timestep i
    count <- size                # begin with count=(nx,ny,...,nt), reads entire var
    count[dims] <- 1             # change to count=(nx,ny,...,1) to read 1 tstep
    
    dt<-ncvar_get(nc, varid = 'sst', start = start, count = count)
    
    # convert to raster
    r[i]<-raster(dt)
}


dt<-ncvar_get(nc, varid = 'geophysical_data/sst')
r <- raster(dt)
# create layer stack with time dimension
r<-stack(r)

# transpose the raster to have correct orientation


# plot the result
plot(r)


ras <- "C:\\Users\\lxiao\\Desktop\\20201019\\SST_pro.tif"
ref<- raster(ras)
C <- crs(ref)

test <- flip(flip(t(r),1),2)
extent(test) <- extent(ref)

crs(test) <- "+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"


plot(test)
plot(ref[[1]])
writeRaster(r,out,overwrite = T)

"+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"


pro <- projectRaster(r_f, crs=C, res=0.0125875109806657)






library(raster)
library(rgdal)
tif1 <- "C:\\Users\\lxiao\\Desktop\\20201019\\AQUA_MODIS.20170505T185510.L2.SST.nc_reprojected.tif"
tif2 <- "C:\\Users\\lxiao\\Desktop\\20201019\\AQUA_MODIS.20170505T190011.L2.SST.nc_reprojected.tif"
out <- "C:\\Users\\lxiao\\Desktop\\20201019\\mosaic.tif"
r1 <- stack(tif1)
r2 <- stack(tif2)

x <- list(r1,r2)
names(x)[1:2] <- c('x', 'y')
x$fun <- max
x$na.rm <- TRUE
x$tolerance = 0.5
y <- do.call(mosaic, x)

y <- dropLayer(y, c(2,3,5,6,7,8,9))

writeRaster(y,file=out,overwrite = T)




library(raster)
library(rgdal)

#set R temp location
rasterOptions(tmpdir = "E:/temp/R/")
write("R_USER = E:/temp/R/", file=file.path(Sys.getenv('R_USER'), '.Renviron'))

path <- "E:\\seadas\\rui\\2017\\result\\tif\\reprojection"
out_path <- "E:\\seadas\\rui\\2017\\result\\tif\\mosaic"
p <- c("OC20170627")
print(p)
c <- 1
x <- list()
list<-(list.files(path = path, 
                  pattern = p,full.names = T))
print(list)
for(i in list){
    x[[c]] <-stack(i)
    c <- c+1
}
names(x)[1:2] <- c('x', 'y')
x$fun <- max
x$na.rm <- TRUE
x$tolerance = 0.5
y <- do.call(mosaic, x)
if (p == "OC20170516"){
    y <- dropLayer(y, c(1,2,14,16,17,18,19,20,21,22,23))
    out <- file.path(out_path,paste0(p,'_mosaic.tif'))
    writeRaster(y,file=out,overwrite = T)
}else if (p == "OC20170516"){
    y <- dropLayer(y, c(2,3,5,6,7,8,9))
    out <- file.path(out_path,paste0(p,'_mosaic.tif'))
    writeRaster(y,file=out,overwrite = T)
}
print(out)


