document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll(".cat-link").forEach(function(link) {
        link.onclick = function() {
            objects_by_category(link.dataset.category);
        }
    });

    document.querySelectorAll(".my-cat-link").forEach(function(link) {
        link.onclick = function() {
            my_objects_by_category(link.dataset.category);
        }
    });

    const search_box = document.querySelector('.compendium-search');
    if (search_box) {
        document.querySelector('.search-button').onclick = search;
    }

    const my_browser = document.querySelector(".my-browser");
    if (my_browser) {
        my_browser.onclick = display_my_browser;
    }

    const my_todo = document.querySelector(".my-todo");
    if (my_todo) {
        my_todo.onclick = display_todo;
    }
})


function search() {
    const list = document.querySelector('.search-list');
    clear_children(list);
    const search = document.querySelector('.compendium-search').value.toLowerCase();
    var counter = 0;

    fetch('https://botw-compendium.herokuapp.com/api/v3/compendium/all')
        .then(response => response.json())
        .then(json => {
            json['data'].forEach(item => {
                if (item['name'].includes(search)) {
                    list.appendChild(construct_li(item))
                    counter++;
                }
            })
        })
}

function objects_by_category(category) {
    const list = document.querySelector('.item-list');
    clear_children(list);

    fetch('https://botw-compendium.herokuapp.com/api/v3/compendium/category/' + category)
        .then(response => response.json())
        .then(json => {
            json['data'].forEach(item => {
                li = construct_li(item);
                list.appendChild(li);
            });
        });
}

async function my_objects_by_category(category) {
    const list = document.querySelector('.my-item-list');
    clear_children(list);

    try {
        const completionsResponse = await fetch('/completed/');
        if (!completionsResponse.ok) {
            throw new Error('failed to fetch completions');
        }

        const completions = await completionsResponse.json();

        const externalApiReponse = await fetch('https://botw-compendium.herokuapp.com/api/v3/compendium/category/' + category);
        if (!externalApiReponse.ok) {
            throw new Error('external fetch failed');
        }

        const json = await externalApiReponse.json();

        json['data'].forEach(item => {
            if (!completions.includes(item['id'])) {
                const li = construct_li(item);
                list.appendChild(li);
            }
        });
    } catch (error) {
        console.error('error', error);
    }
}


function clear_children(parent) {
    var child = parent.lastElementChild;
    while (child) {
        parent.removeChild(child);
        child = parent.lastElementChild;
    }
}


function construct_li(item) {
    const new_item = document.createElement('li');
    const new_link = document.createElement('a');
    new_link.href = `/entry/${item.id}`;

    new_link.textContent = to_title_case(item['name']);
    new_item.appendChild(new_link);
    return new_item;
}

function to_title_case(s) {
    let parts = s.split(" ");
    for (let i = 0; i < parts.length; i++) {
        parts[i] = parts[i].charAt(0).toUpperCase() + parts[i].slice(1);
    }
    if (parts.length == 3) {
        if (parts[0] === "Guardian" && parts[1] === "Scout") {
            parts[2] = parts[2].toUpperCase();
        }
    }
    return parts.join(" ");
}

function toggle_collect(id) {
    fetch('../../togglecollection/' + id, {
        method: "PUT",
        body: JSON.stringify({
            "collect": true
        })
    })

    const button = document.querySelector(".toggle-complete-button");
    if (button.textContent === "Complete") {
        button.textContent = "Uncomplete";
    } else {
        button.textContent = "Complete";
    }
}


function toggle_todo(id) {
    fetch('../../toggletodo/' + id, {
        method: "PUT",
        body: JSON.stringify({
            "todo": true
        })
    })

    const button = document.querySelector(".toggle-todo-button");
    if (button.textContent === "Add to todo") {
        button.textContent = "Remove from todo";
    } else {
        button.textContent = "Add to todo";
    }
}


function display_todo() {
    const browser = document.querySelector(".my-browser-div")
    const todo = document.querySelector(".my-todo-div")
    const list = document.querySelector(".todo-list")

    browser.style.display = 'none';
    todo.style.display = 'block';

    fetch('/todo/')
        .then(response => response.json())
        .then(data => {
            data.forEach(todo_item => {
                fetch('https://botw-compendium.herokuapp.com/api/v3/compendium/entry/' + todo_item)
                    .then(response => response.json())
                    .then(data => {
                        const li = construct_li(data['data']);
                        list.appendChild(li);
                    })
            })
        })
}


function display_my_browser() {
    const browser = document.querySelector(".my-browser-div")
    const todo = document.querySelector(".my-todo-div")

    browser.style.display = 'block';
    todo.style.display = 'none';
}