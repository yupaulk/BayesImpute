library(splatter)
params <- newSplatParams(batchCells = 3000, nGenes = 1500, 
                         group.prob = c(0.2,0.35,0.45), 
                         de.prob = 0.045,
                         de.facLoc = 0.1,
                         de.facScale = 0.4,
                         dropout.mid = 0.2,
                         seed = 42)

sim <- splatSimulateGroups(params, verbose = TRUE)
simcounts <- counts(sim)

write.table(t(simcounts), file='raw_counts.csv', quote=FALSE, sep='\t', col.names = NA)
write.table(sim$Group, file='label.csv', quote=FALSE, sep='\t', col.names = NA)