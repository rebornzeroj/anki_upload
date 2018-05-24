from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.utils import fmtTimeSpan
from anki.stats import CollectionStats
import urllib2
import json
import time
import threading
from upload_stats.upload import http_post

def sync():
	cs = CollectionStats(mw.col)
	cs.wholeCollection = True
	lims = []
	num = 365
	chunk = 1
	if num is not None:
		lims.append("id > %d" % (
			(cs.col.sched.dayCutoff-(num*chunk*86400))*1000))
	lim = cs._revlogLimit()
	if lim:
		lims.append(lim)
	if lims:
		lim = "where " + " and ".join(lims)
	else:
		lim = ""
	if cs.type == 0:
		tf = 60.0 # minutes
	else:
		tf = 3600.0 # hours
	revlog = cs.col.db.all("""
	select
	(cast((id/1000.0 - :cut) / 86400.0 as int))/:chunk as day,
	sum(time)/1000,
	sum(case when type = 0 then 1 else 0 end), -- lrn count
	sum(case when type = 1 and lastIvl < 21 then 1 else 0 end), -- yng count
	sum(case when type = 1 and lastIvl >= 21 then 1 else 0 end), -- mtr count
	sum(case when type = 2 then 1 else 0 end), -- lapse count
	sum(case when type = 3 then 1 else 0 end), -- cram count
	sum(case when type = 0 then time/1000.0 else 0 end)/:tf, -- lrn time
	-- yng + mtr time
	sum(case when type = 1 and lastIvl < 21 then time/1000.0 else 0 end)/:tf,
	sum(case when type = 1 and lastIvl >= 21 then time/1000.0 else 0 end)/:tf,
	sum(case when type = 2 then time/1000.0 else 0 end)/:tf, -- lapse time
	sum(case when type = 3 then time/1000.0 else 0 end)/:tf -- cram time
	from revlog %s
	group by day order by day""" % lim,
						cut=cs.col.sched.dayCutoff,
						tf=tf,
						chunk=chunk)
	

	values = {'data': revlog, 'email': mw.pm.profile.get('syncUser')} 
	html = http_post(values)
	
	showInfo(html)
	
sync_action = QAction("Upload Stats", mw)
sync_action.triggered.connect(sync)
mw.form.menuTools.addAction(sync_action)