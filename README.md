## gatherTweet

gatherTweet is a Python package wrapper used for:

- Creating cohesive data object for events with spatially and temporally disperced groups of activities
- Find individuals who participate in each individual activity - the core
- Explore the timeline of individuals in the core
- Find individuals who either echo or influence the core
- Explore the timeline of echos and influences
- Perform basic analysis on the results

# Installation 

In order to install using pip write

```
pip install git+https://github.com/ckann10/gatherTweet.git
```

The module along with all of it's packages can then be imported into your Python script using

```
import gatherTweet
```



# Key Files

- gatherNet_documentation.pdf - detailed documentation of the program
- event_template.xlsx - template to fill TwitterEvent objects, filled with all the information except for Twitter API keys in order to run the example
- examples - easy to follow examples to further understand functionality of package

# Examples

There are currently two example scripts which must be explored in order.

example-pull_core_and_timeline.py -

Uses the Excel template provided in the github repo to pull the Core and Timeline for individuals during a small BLM protest in Houston. In order to run the file a copy of the excel sheet needs to be placed in the folder called "dirr" and needs to be populated with individual Twitter Access keys. The sheet can be updated to your particular purpose.

example-analyze_data.py -

After the Core and Timeline has been pulled, this funtion shows how to move the json files into a usable format.





  
