// ---------------- BOOKS ----------------
function loadBooks() {
    fetch("/api/books").then(r => r.json()).then(data => {
        let html = "<tr><th>ID</th><th>Title</th><th>Author</th><th>Copies</th><th>Action</th></tr>";
        data.forEach(b => {
            html += `<tr>
                <td>${b.id}</td>
                <td>${b.title}</td>
                <td>${b.author}</td>
                <td>${b.copies}</td>
                <td><button onclick="delBook(${b.id})">Delete</button></td>
            </tr>`;
        });
        document.getElementById("bookTable").innerHTML = html;
    });
}

function addBook() {
    let data = {
        title: document.getElementById("btitle").value,
        author: document.getElementById("bauthor").value,
        copies: parseInt(document.getElementById("bcopies").value)
    };
    fetch("/api/books", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    }).then(() => loadBooks());
}

function delBook(id) {
    fetch("/api/books/" + id, {method:"DELETE"}).then(() => loadBooks());
}

// ---------------- STUDENTS ----------------
function loadStudents() {
    fetch("/api/students").then(r => r.json()).then(data => {
        let html = "<tr><th>ID</th><th>Name</th><th>Roll</th><th>Action</th></tr>";
        data.forEach(s => {
            html += `<tr>
                <td>${s.id}</td>
                <td>${s.name}</td>
                <td>${s.roll_no}</td>
                <td><button onclick="delStudent(${s.id})">Delete</button></td>
            </tr>`;
        });
        document.getElementById("studentTable").innerHTML = html;
    });
}

function addStudent() {
    let data = {
        name: document.getElementById("sname").value,
        roll_no: document.getElementById("sroll").value
    };
    fetch("/api/students", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    }).then(() => loadStudents());
}

function delStudent(id) {
    fetch("/api/students/" + id, {method:"DELETE"}).then(() => loadStudents());
}

// ---------------- ISSUE / RETURN ----------------
function loadIssuePage() {
    loadIssueBooks();
    loadIssueStudents();
    loadIssuedList();
}

function loadIssueStudents() {
    fetch("/api/students").then(r => r.json()).then(data => {
        let s = document.getElementById("studentSelect");
        // clear existing options
        s.innerHTML = "<option value=\"\">Select student</option>";
        data.forEach(st => {
            s.innerHTML += `<option value="${st.id}">${st.name} (${st.roll_no})</option>`;
        });
    });
}

function loadIssueBooks() {
    fetch("/api/books").then(r => r.json()).then(data => {
        let b = document.getElementById("bookSelect");
        b.innerHTML = "<option value=\"\">Select book</option>";
        data.forEach(book => {
            b.innerHTML += `<option value="${book.id}">${book.title}</option>`;
        });
    });
}

function issueBook() {
    let data = {
        student_id: parseInt(document.getElementById("studentSelect").value),
        book_id: parseInt(document.getElementById("bookSelect").value)
    };
    fetch("/api/issue", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    }).then(() => loadIssuedList());
}

function loadIssuedList() {
    fetch("/api/issued").then(r => r.json()).then(data => {
        let html = "<tr><th>ID</th><th>Student</th><th>Book</th><th>Issued</th><th>Returned</th><th>Action</th></tr>";
        data.forEach(i => {
            const returnCell = i.return_date ? "" : `<button onclick="returnBook(${i.id})">Return</button>`;
            html += `<tr>
                <td>${i.id}</td>
                <td>${i.student}</td>
                <td>${i.book}</td>
                <td>${i.issue_date}</td>
                <td>${i.return_date || "-"}</td>
                <td>${returnCell}</td>
            </tr>`;
        });

        document.getElementById("issueTable").innerHTML = html;
    });
}

function returnBook(id) {
    fetch("/api/return/" + id, {method:"POST"}).then(() => loadIssuedList());
}