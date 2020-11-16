function ViewPost(post_id, user) {
    fetch("/API/post/" + post_id)
        .then(blog => blog.json())
        .then(post => {
            title = document.createElement("h1");
            title.innerText = post.title;
            document.body.appendChild(title);

            var image = document.createElement("img");
            image.setAttribute("src", post.image);
            image.classList.add("image");
            image.setAttribute("alt", "post image");
            document.body.appendChild(image);

            var ownerAndDate = document.createElement("p");
            ownerAndDate.innerText = "By " + post.owner + " on " + post.created_at;
            document.body.appendChild(ownerAndDate);

            var content = document.createElement("pre");
            content.innerText = post.content;
            document.body.appendChild(content);

            if (user == post.owner || user == "admin") {
                var edit = document.createElement("a");
                edit.innerText = "Edit";
                edit.href = "/edit/" + post_id;
                edit.classList.add("button");
                document.body.appendChild(edit);

                var deleteButton = document.createElement("a");
                deleteButton.innerText = "Delete";
                deleteButton.href = "/delete/" + post_id;
                deleteButton.classList.add("button");
                deleteButton.setAttribute("onclick", 'return confirm("Are you sure you want to delete this?")');
                document.body.appendChild(deleteButton);

            }

        });
}