#!/bin/bash

clear; time python launcher.py scrape_basketball_reference source=site season=2013 yesterday_only=true

clear; time python launcher.py scrape_basketball_reference source=site season=2013 type=teams yesterday_only=true

clear; time python launcher.py fantasy_point_calculator site=DRAFT_DAY season=2013
clear; time python launcher.py fantasy_point_calculator site=DRAFT_KINGS season=2013
clear; time python launcher.py fantasy_point_calculator site=FAN_DUEL season=2013
clear; time python launcher.py fantasy_point_calculator site=STAR_STREET season=2013

clear; time python launcher.py determine_injuries season=2013 type=previous
clear; time python launcher.py determine_injuries season=2013 type=current

clear; time python launcher.py fix_injuries 2013

# Calculate Defense-vs-position
clear; time python launcher.py calculate_dvp_rank season=2013 yesterday_only=true