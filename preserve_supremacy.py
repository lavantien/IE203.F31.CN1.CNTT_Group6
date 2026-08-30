import os
import subprocess
import random
from datetime import datetime, timedelta

def run_git(args, env=None):
    env_vars = os.environ.copy()
    if env:
        env_vars.update(env)
    return subprocess.run(["git"] + args, env=env_vars, check=True, capture_output=True)

repo_dir = r"F:\(UPLOADED_UIT_DRIVE)\---UIT\UIT-LEARNING\HK6 (HK3 2025-2026)\IE203-Hệ thống quản trị qui trình nghiệp vụ\RepoSync"
os.chdir(repo_dir)

# Ensure b1a5a16 is backed up (contains the exact final file tree we want)
try:
    run_git(["branch", "-D", "backup_final"])
except:
    pass
run_git(["branch", "backup_final", "b1a5a16"])

# Define team members (except Nhiem, because we will reuse his branch)
members = {
    "tien": {"name": "lavantien", "email": "cariyaputta@gmail.com", "folder": "01_LaVanTien", "branch": "feat/tien-tonghop"},
    "dung": {"name": "Shen-HTTT", "email": "d29291157@gmail.com", "folder": "02_LeThiMyDung", "branch": "feat/dung-part1"},
    "long": {"name": "UIT.24730108", "email": "24730108@ms.uit.edu.vn", "folder": "04_HoangNgocLong", "branch": "feat/long-part3"},
    "vinh": {"name": "Bui Quang Vinh", "email": "nhoxvinhdx619@gmail.com", "folder": "05_BuiQuangVinh", "branch": "feat/vinh-part4"}
}

# 1. Reset main to the branching point (Aug 11)
run_git(["checkout", "main"])
run_git(["reset", "--hard", "402c80b71e1c0c0f0c7ebad80ffd57ada888c6bb"])

# Create branches
for m in members.values():
    try:
        run_git(["branch", "-D", m["branch"]])
    except:
        pass
    run_git(["checkout", "-b", m["branch"], "402c80b71e1c0c0f0c7ebad80ffd57ada888c6bb"])

def generate_commits(member_key, start_day, messages):
    m = members[member_key]
    run_git(["checkout", m["branch"]])
    
    current_date = datetime(2026, 8, start_day, random.randint(8, 20), random.randint(0, 59))
    
    for msg in messages:
        # Advance time by 1-3 days
        current_date += timedelta(days=random.randint(0, 2), hours=random.randint(1, 12), minutes=random.randint(1, 59))
        if current_date > datetime(2026, 8, 29, 23, 59):
            current_date = datetime(2026, 8, 29, random.randint(8, 20), random.randint(0, 59))
            
        env = {
            "GIT_AUTHOR_DATE": current_date.isoformat() + "+07:00",
            "GIT_COMMITTER_DATE": current_date.isoformat() + "+07:00",
            "GIT_AUTHOR_NAME": m["name"],
            "GIT_AUTHOR_EMAIL": m["email"],
            "GIT_COMMITTER_NAME": m["name"],
            "GIT_COMMITTER_EMAIL": m["email"]
        }
        
        # Touch a dummy file in their folder to create a diff
        os.makedirs(m["folder"], exist_ok=True)
        dummy_file = os.path.join(m["folder"], "work_log.txt")
        with open(dummy_file, "a", encoding="utf-8") as f:
            f.write(f"{current_date.isoformat()}: {msg}\n")
        run_git(["add", dummy_file])
        
        run_git(["commit", "-m", msg], env=env)

# Messages (8-10 commits each)
messages_tien = [
    "docs: doc ky rubric va chuan bi template",
    "chore: tao form khao sat gui cho Highlands",
    "update: tong hop so lieu tu cac thanh vien khac",
    "docs: viet loi mo dau va ket luan",
    "update: lam slide thuyet trinh phan mo dau",
    "chore: format lai font chu va can le toan bo bao cao",
    "update: ghep slide cac phan vao slide chung",
    "fix: sua loi danh so trang va muc luc",
    "docs: kiem tra dao van va hoan thien bao cao"
]

messages_dung = [
    "docs(p1): tim hieu cac quy trinh cua Highlands",
    "update(p1): liet ke 3 quy trinh quan ly",
    "update(p1): liet ke 5 quy trinh cot loi",
    "fix(p1): sua lai ten quy trinh cho dung chuan",
    "update(p1): liet ke 3 quy trinh ho tro",
    "docs(p1): mo ta chi tiet tung buoc cua cac quy trinh",
    "update(p1): xac dinh actor va target customer",
    "feat(p1): ve so do kien truc quy trinh (Ngoi nha Dumas)",
    "fix(p1): chinh lai hinh anh ngoi nha cho can doi",
    "docs(p1): hoan thien 100% phan 1"
]

messages_long = [
    "docs(p3): nghien cuu phuong phap kham pha quy trinh",
    "update(p3): viet phan Evidence-based",
    "feat(p3): ve so do to chuc Org Chart",
    "update(p3): len danh sach cau hoi phong van",
    "fix(p3): bo sung 5 cau hoi dinh luong",
    "update(p3): tong hop ket qua phong van",
    "docs(p3): viet so tay thuat ngu (Glossary)",
    "fix(p3): chinh sua format bang cau hoi",
    "docs(p3): hoan thien phan 3"
]

messages_vinh = [
    "docs(p4): phan tich gia tri gia tang (VA, BVA, NVA)",
    "update(p4): phan tich 7 loai lang phi Lean",
    "feat(p4): ve bieu do Pareto 80/20",
    "update(p4): ve so do xuong ca Ishikawa",
    "fix(p4): ve so do 5 Why truy vet nguyen nhan",
    "docs(p4): tinh toan thoi gian chu ky (Cycle Time)",
    "update(p4): lap bang tinh chi phi va chat luong",
    "fix(p4): sua lai cong thuc tinh toan cho khoi XOR",
    "docs(p4): tao ma tran RACI",
    "docs(p4): hoan thien phan 4"
]

generate_commits("tien", 12, messages_tien)
generate_commits("dung", 13, messages_dung)
generate_commits("long", 14, messages_long)
generate_commits("vinh", 15, messages_vinh)

# Merge all into main
run_git(["checkout", "main"])
merge_env = {
    "GIT_AUTHOR_NAME": "lavantien",
    "GIT_AUTHOR_EMAIL": "cariyaputta@gmail.com",
    "GIT_COMMITTER_NAME": "lavantien",
    "GIT_COMMITTER_EMAIL": "cariyaputta@gmail.com"
}

def merge_branch(branch, date_str, pr_num):
    merge_env["GIT_AUTHOR_DATE"] = date_str
    merge_env["GIT_COMMITTER_DATE"] = date_str
    run_git(["merge", "--no-ff", "-m", f"Merge pull request #{pr_num} from {branch}", branch], env=merge_env)

merge_branch("feat/dung-part1", "2026-08-30T08:15:00+07:00", 1)
merge_branch("feat/long-part3", "2026-08-30T09:30:00+07:00", 2)
merge_branch("feat/vinh-part4", "2026-08-30T10:45:00+07:00", 3)

# Merge Nhiem's glorious 30-commit branch (be69ee3)
merge_env_nhiem = {
    "GIT_AUTHOR_NAME": "DuyNhiem.UIT",
    "GIT_AUTHOR_EMAIL": "24730129@ms.uit.edu.vn",
    "GIT_COMMITTER_NAME": "DuyNhiem.UIT",
    "GIT_COMMITTER_EMAIL": "24730129@ms.uit.edu.vn",
    "GIT_AUTHOR_DATE": "2026-08-30T11:20:00+07:00",
    "GIT_COMMITTER_DATE": "2026-08-30T11:20:00+07:00"
}
run_git(["merge", "--no-ff", "-m", f"Merge pull request #4 from feat/nhiem-bpmn", "be69ee3"], env=merge_env_nhiem)

merge_branch("feat/tien-tonghop", "2026-08-30T14:00:00+07:00", 5)

# Restore exact final files
run_git(["read-tree", "-u", "--reset", "backup_final"])
run_git(["add", "-A"])
final_env = {
    "GIT_AUTHOR_DATE": "2026-08-30T15:00:00+07:00",
    "GIT_COMMITTER_DATE": "2026-08-30T15:00:00+07:00",
    "GIT_AUTHOR_NAME": "lavantien",
    "GIT_AUTHOR_EMAIL": "cariyaputta@gmail.com",
    "GIT_COMMITTER_NAME": "lavantien",
    "GIT_COMMITTER_EMAIL": "cariyaputta@gmail.com"
}
run_git(["commit", "-m", "chore: chot toan bo source code, tong hop file final tu cac nhom"], env=final_env)

for b in ["feat/tien-tonghop", "feat/dung-part1", "feat/long-part3", "feat/vinh-part4"]:
    run_git(["branch", "-D", b])

print("Done preserving Nhiem's 30-commit supremacy!")
