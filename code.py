import streamlit as st

# Page configuration
st.set_page_config(page_title="Relationship & Task Tracker", page_icon="✨", layout="centered")

# Initialize mock session state data
if "tasks" not in st.session_state:
    st.session_state.tasks = [{"task": "Complete your daily posture check", "status": "Pending", "notes": ""}]
if "logs" not in st.session_state:
    st.session_state.logs = []
if "sub_role" not in st.session_state:
    st.session_state.sub_role = "Devoted Partner"
if "rewards" not in st.session_state:
    st.session_state.rewards = [
        {"reward": "Custom massage or spa night", "status": "Available"},
        {"reward": "Special treat of her choice", "status": "Claimed"}
    ]

st.title("💖 Shared Growth & Task Hub")

# Simple role selector for testing
role = st.sidebar.selectbox("Select View", ["Partner View (sub)", "Admin View (dom)"])

if role == "Admin View (dom)":
    st.header("Admin Management Panel")
    
    # 1. Sub's Title / Role configuration
    st.subheader("Submissive Title / Role")
    st.write("Set or update the active title or role for your partner to see on her dashboard.")
    with st.form("role_form"):
        new_role_title = st.text_input("Active Title / Role:", value=st.session_state.sub_role)
        role_submitted = st.form_submit_button("Update Role")
        if role_submitted and new_role_title:
            st.session_state.sub_role = new_role_title
            st.success(f"Role updated to: '{new_role_title}'")

    st.markdown("---")

    # 2. Task Assignment
    st.header("Task Assignment")
    st.write("Assign new tasks or power-play prompts for your partner.")
    
    with st.form("new_task_form"):
        new_task = st.text_input("New Task / Reminder:")
        submitted = st.form_submit_button("Assign Task")
        if submitted and new_task:
            st.session_state.tasks.append({"task": new_task, "status": "Pending", "notes": ""})
            st.success(f"Task assigned: '{new_task}'")

    st.subheader("Current Active Tasks")
    for idx, t in enumerate(st.session_state.tasks):
        st.write(f"- **{t['task']}** [Status: *{t['status']}*]")

    st.markdown("---")

    # 3. Rewards Management (Bug-Free Form Approach)
    st.header("Rewards Management")
    st.write("Manually add and manage rewards that she can view.")
    
    with st.form("new_reward_form"):
        new_reward_text = st.text_input("New Reward Description:")
        reward_status = st.selectbox("Initial Status:", ["Available", "Claimed", "Locked"])
        reward_submitted = st.form_submit_button("Add Reward")
        if reward_submitted and new_reward_text:
            st.session_state.rewards.append({"reward": new_reward_text, "status": reward_status})
            st.success(f"Reward added: '{new_reward_text}'")

    st.subheader("Current Reward Pool & Status Updates")
    
    with st.form("update_rewards_form"):
        updated_statuses = []
        for r_idx, r in enumerate(st.session_state.rewards):
            st.write(f"**{r['reward']}**")
            current_status_idx = ["Available", "Claimed", "Locked"].index(r['status'])
            new_status = st.selectbox(
                f"Status for reward {r_idx + 1}", 
                ["Available", "Claimed", "Locked"], 
                index=current_status_idx, 
                key=f"admin_reward_status_{r_idx}"
            )
            updated_statuses.append(new_status)
            st.markdown("---")
            
        update_rewards_btn = st.form_submit_button("Save Reward Status Changes")
        if update_rewards_btn:
            for r_idx, status in enumerate(updated_statuses):
                st.session_state.rewards[r_idx]['status'] = status
            st.success("Reward statuses updated successfully!")

    st.subheader("Her Performance Logs")
    if st.session_state.logs:
        for log in st.session_state.logs:
            st.info(f"**Task:** {log['task']}  \n**Rating:** {log['rating']}/5  \n**Notes:** {log['notes']}")
    else:
        st.write("No logs submitted yet.")

else:
    # Partner / Sub View
    st.header("Your Daily Tasks & Standing")
    
    # Display current assigned role/title prominently
    st.info(f"👑 **Current Role / Title:** {st.session_state.sub_role}")
    
    st.write("Check your active tasks below, complete them, and log your thoughts!")

    if not st.session_state.tasks:
        st.write("No tasks assigned right now! Check back later.")
    else:
        for idx, t in enumerate(st.session_state.tasks):
            st.subheader(f"Task {idx + 1}: {t['task']}")
            
            with st.form(f"log_form_{idx}"):
                rating = st.slider("How did you feel about this? (1-5)", 1, 5, 3, key=f"slider_{idx}")
                notes = st.text_area("How did it go? What can be improved?", key=f"text_{idx}")
                complete_btn = st.form_submit_button("Submit & Complete")
                
                if complete_btn:
                    st.session_state.tasks[idx]["status"] = "Completed"
                    st.session_state.tasks[idx]["notes"] = notes
                    st.session_state.logs.append({
                        "task": t["task"],
                        "rating": rating,
                        "notes": notes
                    })
                    st.success("Great job! Log submitted successfully.")

    st.markdown("---")
    
    # Rewards section visible to the sub
    st.header("🎁 Available Rewards & Privileges")
    st.write("Here are the current rewards and their statuses set by your Dom/Partner:")
    
    if not st.session_state.rewards:
        st.write("No rewards listed yet.")
    else:
        for r in st.session_state.rewards:
            st.write(f"- **{r['reward']}** — Status: *{r['status']}*")
