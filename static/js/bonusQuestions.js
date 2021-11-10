// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        items.sort((first, second) => {
            return compareObjects(first, second, sortField)
        })
    } else {
        items.sort((first, second) => {
            return compareObjects(first, second, sortField)
        }).reverse()
    }

    function compareObjects(object1, object2, key){
        const obj1 = object1[key].toUpperCase()
        const obj2 = object2[key].toUpperCase()
        if (obj1 < obj2) {
            return -1
        }
        if (obj1 > obj2) {
            return 1
        }
        return 0
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //

    if (filterValue[0] === '!'){
        if (filterValue.includes('Description:')){
            items = items.filter(item => !item.Description.includes(filterValue.slice(13)))
            return items
        }
        items = items.filter(item => !item.Title.includes(filterValue.slice(1)))
    } else {
        if (filterValue.includes('Description:')){
            items = items.filter(item => item.Description.includes(filterValue.slice(12)))
            return items
        }
        items = items.filter(item => item.Title.includes(filterValue))
    }

    return items
}

function toggleTheme() {
    console.log("toggle theme")
    let body = document.getElementsByTagName("body");
    let style = window.getComputedStyle(body[0]).getPropertyValue('background-color');
    if (style === "rgb(0, 0, 0)") {
        body[0].style.backgroundColor = "White"
        body[0].style.color = "Black"
    } else {
        body[0].style.backgroundColor = "Black"
        body[0].style.color = "White"
    }
}

function increaseFont() {
    console.log("increaseFont")
    let elements = document.getElementsByTagName("td");
    for (let i=0; i<elements.length; i++){
        let currentSize = parseFloat(window.getComputedStyle(elements[i], null).getPropertyValue('font-size'));
        if (currentSize < 15) {
            elements[i].style.fontSize = (currentSize + 1) + "px";
        }
    }
}

function decreaseFont() {
    console.log("decreaseFont")
    let elements = document.getElementsByTagName("td")
    for (let i=0; i<elements.length; i++){
        let currentSize = parseFloat(window.getComputedStyle(elements[i], null).getPropertyValue('font-size'));
        if (currentSize > 3) {
            elements[i].style.fontSize = (currentSize - 1) + "px";
        }
    }
}