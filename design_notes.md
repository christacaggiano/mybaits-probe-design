## Notes from Mybaits 

* **Goal:** bisulfite treat DNA --> capture --> sequence 
* **Expectation** most of the CpGs will be closed, but we are most interested in open CpGs 
* non-bisulfite treated DNA is assumed to be the reference 
* Baits should focus on the various bisulfite sequences that are methylated/unmethylated 
    * use read data that uses observed reads to build probe sets 
* 90-mer proposed but would result in >40,000 baits for ~1,000 CpGs 
    * 72-mer base is enough for to pull down a DNA fragment 
* Baits included for fully methylated/bisulfite converted 
* Baits are densely tiled, but 1 bait can pull down 300-mer
    * can identify important sites that need to be pulled down, and other locations can be less densely tiled 
* to identify rarer "open CpGs" that may come from tissues like brain etc, want to capture these states. Want to capture a core CpG of interest + 2 flanking CpGs (haplotyping blocks) 
* Rank order CpGs based on importance 
* ~40,000 baits $4850/16 reactions. <8/capture reaction to prevent drop out and capture rare events. =~120 individuals reaction. Main cost is library preperation 
* ~60,000 baits ~5800/16 reactions  