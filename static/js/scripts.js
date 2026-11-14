
document.addEventListener("DOMContentLoaded", function () {
    console.log("Dokandar JavaScript is working!");
});
 document.addEventListener("click", function (event) {
            document.querySelectorAll(".profile-menu.profile-open")
                .forEach(function (menu) {
                    if (!menu.contains(event.target)) {
                        menu.classList.remove("profile-open");

                        const link = menu.querySelector(".profile-link");
                        if (link) {
                            link.setAttribute("aria-expanded", "false");
                        }
                    }
                });
        });

        // Close dropdown with Escape key
        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                document.querySelectorAll(".profile-menu.profile-open")
                    .forEach(function (menu) {
                        menu.classList.remove("profile-open");

                        const link = menu.querySelector(".profile-link");
                        if (link) {
                            link.setAttribute("aria-expanded", "false");
                            link.focus();
                        }
                    });
            }
        });