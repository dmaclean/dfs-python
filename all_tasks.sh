#!/bin/bash

clear; time python basketball.py source=site season=2013 yesterday_only=true

clear; time python basketball.py source=site season=2013 type=teams yesterday_only=true

clear; time python fantasy_point_calculator.py site=DRAFT_DAY season=2013
clear; time python fantasy_point_calculator.py site=DRAFT_KINGS season=2013
clear; time python fantasy_point_calculator.py site=FAN_DUEL season=2013
clear; time python fantasy_point_calculator.py site=STAR_STREET season=2013

clear; time python determine_injuries.py season=2013 type=previous
clear; time python determine_injuries.py season=2013 type=current

# Calculate Defense-vs-position
clear; time python calculate_dvp_rank.py season=2013 yesterday_only=true