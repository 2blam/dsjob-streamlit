import streamlit as st
from datetime import date, datetime, time, timedelta
import pymongo
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# use wide screen
st.set_page_config(layout="wide")

# Initialize connection.
client = pymongo.MongoClient(**st.secrets["mongo"])
def get_fig_location(from_date, to_date):
	db = client.dsjob

	query = {"post_date": {
				"$gte": datetime.combine(from_date, time.min), 
				"$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
				}
			}

	r = db.jobad.find(query, {"location"})
	r = list(r)

	# tidy
	lst = [e['location'] for e in r]
	lst = tidy_address(lst)

	df_result = pd.DataFrame({'location': lst})

	df_result = df_result.groupby(["location"]).size().reset_index()
	df_result.columns = ["location", "cnt"]
	#df_result["pct"] = df_result.cnt / df_result.cnt.sum() * 100

	location = df_result["location"].tolist()
	cnt = df_result["cnt"].tolist()

	fig = go.Figure()

	fig.add_trace(go.Pie(labels=location, values=cnt, hole=.3))

	fig.update_layout(title="Job Location")

	return fig

def get_fig_keyword_count(from_date, to_date, top_n=10):
	db = client.dsjob

	result = db.tskeywordcount.find({"date": {
                            "$gte": datetime.combine(from_date, time.min), 
                            "$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
                            }
                    }, {"date", "keyword", "cnt"})

	df_keyword = pd.DataFrame(result)
	df_keyword_top_n = df_keyword.groupby(["keyword"]).sum("cnt").reset_index().sort_values("cnt", ascending=False).head(top_n).reset_index(drop=True)

	df_keyword_top_n.columns = ["Keyword", "Count"]
	x = df_keyword_top_n["Keyword"].tolist()
	y = df_keyword_top_n["Count"].tolist()
	x.reverse()
	y.reverse()
	
	fig = go.Figure()

	fig.add_trace(go.Bar(
		x=y,
		y=x,
		marker=dict(
			color='rgba(50, 171, 96, 0.6)',
		),		
		name = "Keyword(s)",
		orientation='h',
		))

	fig.update_layout(
	    title="Top N Keyword(s)",
	    xaxis_title="Count",
	    yaxis_title="Keyword",
	    
	)

	return fig

def get_fig_skill_count(from_date, to_date, top_n=10):
	db = client.dsjob

	result = db.tsskillcount.find({"date": {
                            "$gte": datetime.combine(from_date, time.min), 
                            "$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
                            }
                    }, {"date", "skill", "cnt"})

	df_skill = pd.DataFrame(result)
	df_skill_top_n = df_skill.groupby(["skill"]).sum("cnt").reset_index().sort_values("cnt", ascending=False).head(top_n).reset_index(drop=True)
	df_skill_top_n.columns = ["Skill", "Count"]
	x = df_skill_top_n["Skill"].tolist()
	y = df_skill_top_n["Count"].tolist()
	x.reverse()
	y.reverse()
	
	fig = go.Figure()

	fig.add_trace(go.Bar(
		x=y,
		y=x,
		marker=dict(
			color='rgba(53, 155, 288, 0.6)'
		),		
		name = "Skill(s)",
		orientation='h',
		))

	fig.update_layout(
	    title="Top N Skill(s)",
	    xaxis_title="Count",
	    yaxis_title="Skill",
	    
	)

	return fig

def get_fig_job_ad_ts(from_date, to_date):
	db = client.dsjob

	result = db.tsjobadcount.find({"date": {
                        "$gte": datetime.combine(from_date, time.min), 
                        "$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
                        }
                }, {"date", "cnt"})
	result = list(result) 
	
	df = pd.DataFrame(result)
	df = df[["date", "cnt"]]
	df.columns = ["Date", "No. of Job Advertisement"]

	fig = px.line(df, x='Date', y='No. of Job Advertisement', title="No. of Job Advertistments Per Day")

	fig.update_xaxes(rangeslider_visible=True)
	return fig

def get_unique_company_count(from_date, to_date):
	db = client.dsjob
	r = db.jobad.distinct("company",{"post_date": {
							"$gte": datetime.combine(from_date, time.min), 
							"$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
 							}
					})
	return len(r)
	
def tidy_address(lst):
	r_loc = []
	valid_on_loc = ['Toronto, ON', 
			'Mississauga, ON', 
			'Etobicoke, ON', 
			'Brampton, ON', 
			'Scarborough, ON', 
			'Guelph, ON', 
			'London, ON', 
			'Canada', 
			'Thornhill, ON', 
			'Ontario', 
			'North York, ON', 
			'Greater Toronto Area, ON', 
			'Don Mills, ON', 
			'Concord, ON', 
			'Ottawa, ON', 
			'Markham, ON',
			'Vaughan, ON']
	for loc in lst:
		if loc not in valid_on_loc:
			r_loc.append("Others")
		else:
			r_loc.append(loc)
	return r_loc

def get_remote_percentage(from_date, to_date):
	db = client.dsjob
	
	query = {"post_date": {
                                                        "$gte": datetime.combine(from_date, time.min),
                                                        "$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
                                                        }
                                        }
	r = db.jobad.find(query, {"remote_work_type"})
	
	r = list(r)
	lst = [e['remote_work_type'] for e in r] #None, Temporarily Remote, Remote, Hybrid remote
	num_of_remote_job = len(lst) - (lst.count(None))
	return (round(num_of_remote_job / len(lst) * 100))

def get_unique_location(from_date, to_date):
	db = client.dsjob

	query = {"post_date": {
							"$gte": datetime.combine(from_date, time.min), 
							"$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
 							}
					}

	r = db.jobad.find(query, {"location"})
	r = list(r)
	
	# tidy
	lst = [e['location'] for e in r]
	lst = tidy_address(lst)
	return len(set(lst))
	

def get_job_count(from_date, to_date):
	# print("query mongo")
	# print(from_date.strftime("%Y-%m-%d"), to_date.strftime("%Y-%m-%d"))
	db = client.dsjob

	pipeline = [ 
		{ "$match": {"date": {
							"$gte": datetime.combine(from_date, time.min), 
							"$lte": datetime.combine(to_date, time.min) #cast to 00:00:00
 							}
					}
		},
		{ "$group": {"_id": 'null', "total": {"$sum": "$cnt"}}}
	]
	result = db.tsjobadcount.aggregate(pipeline)
	result = list(result) 
	total = result[0]['total']
	return total

# side bar
date_range = []
with st.sidebar:
	min_date = date.today() - timedelta(days=30)
	max_date = date.today()
	date_from = st.date_input("Date From", min_date)
	date_to = st.date_input("Date To", max_date)

	if (date_from is not None and date_to is not None):
		if (date_to >= date_from):
			date_range = [date_from, date_to]
		else:
			st.error("The value of \"Date\" To should be later than \"Date From\"")


# main
st.title("Data Science Related Jobs in Ontario, Toronto")
if len(date_range) == 2:
	col1, col2, col3, col4 = st.columns(4)	
	
	job_count = get_job_count(date_range[0], date_range[1])

	col1.metric("Total Job Post", job_count)

	company_count = get_unique_company_count(date_range[0], date_range[1])
	col2.metric("No. of Unique Company", company_count)

	location_count = get_unique_location(date_range[0], date_range[1])
	col3.metric("No. of Unique Location", location_count)

	col4.metric("Remote Job Percentage", str(get_remote_percentage(date_range[0], date_range[1])) + " %")

	# plot time series chart
	fig_job_ad_ts = get_fig_job_ad_ts(date_range[0], date_range[1])
	st.plotly_chart(fig_job_ad_ts, use_container_width=True)
	
	# plot bar chart - keyword
	col1, col2 = st.columns(2)	
	#fig_top_n_keyword = get_fig_keyword_count(date_range[0], date_range[1], 15)
	#col1.plotly_chart(fig_top_n_keyword, use_container_width=True)

	# plot bar chart - skill
	fig_top_n_skill= get_fig_skill_count(date_range[0], date_range[1], 15)
	col1.plotly_chart(fig_top_n_skill, use_container_width=True)

	fig_location = get_fig_location(date_range[0], date_range[1])
	col2.plotly_chart(fig_location, use_container_width=True)
	pass



