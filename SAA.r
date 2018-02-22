SAA <- function(input,n=4,standardize=FALSE) {
  # takes a data.frame n x m.  n is observations, m is jagged time series.
  # converts to a standard sized time series length arg "n"
  require(TSclust)
  
  input <- as.matrix(input)
  out <- matrix(nrow=nrow(input),ncol=n)
  mu <- rowMeans(input,na.rm=T)
  #if(standardize) {input <- t(scale(t(input)))}
  if(standardize) {input <- log(input/mu)}
  lenvec <- rowSums(!is.na(input))
  for (i in 1:nrow(input)) {
      if(lenvec[i]<=1) {
        out[i,] <- rep(input[i,1],n)
    } else if(lenvec[i] <= n) {
        out[i,] <- approx(x=input[i,!is.na(input[i,])],n=n)$y
    } else { out[i,] <- PAA(x=input[i,!is.na(input[i,])],w=n)
    }
  }
  out[is.inf(out)] <- -1
  out[is.na(out)] <- 0
  return(out)
}

TSkmeans <- function(input,k=5) {
  # takes standard length stacked, time series and produces cluster object
  # includes centers, clusters, centerplot
  require(dplyr)
  require(tidyr)
  require(ggplot2)
  out <- list(NULL)
  km <- kmeans(input,k,iter.max=50,algorithm="Hartigan-Wong")
  kmc <- as.data.frame(km$centers)
  kmc$cluster <- paste0("C",row.names(kmc))
  
  out$centers <- kmc %>%
    gather(time,value,-cluster)
  out$clusters <- paste0("C",km$cluster)
  out$clusplot <- ggplot(data=out$centers, 
                         aes(x=time,y=value,group=as.factor(cluster),
                        color=as.factor(cluster)),label=as.factor(cluster)) + 
                        geom_line(size=1)
  return(out)
}