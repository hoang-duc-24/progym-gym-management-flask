document.addEventListener("DOMContentLoaded", function () {
    const operationLayout = document.getElementById("operationLayout");
    const collapseFilterBtn = document.getElementById("collapseFilterBtn");
    const openFilterBtn = document.getElementById("openFilterBtn");

    if (operationLayout && collapseFilterBtn && openFilterBtn) {
        collapseFilterBtn.addEventListener("click", function () {
            operationLayout.classList.add("filter-collapsed");
            openFilterBtn.classList.remove("d-none");
        });

        openFilterBtn.addEventListener("click", function () {
            operationLayout.classList.remove("filter-collapsed");
            openFilterBtn.classList.add("d-none");
        });
    }

    
    const memberTabs = document.querySelectorAll(".member-tab");
    const memberTabPanels = document.querySelectorAll(".member-tab-panel");

    function activateMemberTab(tabName) {
        if (!tabName || memberTabs.length === 0 || memberTabPanels.length === 0) {
            return;
        }

        const targetTab = document.querySelector(`.member-tab[data-tab="${tabName}"]`);
        const targetPanel = document.getElementById("tab-" + tabName);

        if (!targetTab || !targetPanel) {
            return;
        }

        memberTabs.forEach(function (item) {
            item.classList.remove("active");
        });

        memberTabPanels.forEach(function (panel) {
            panel.classList.remove("active");
        });

        targetTab.classList.add("active");
        targetPanel.classList.add("active");
    }

    if (memberTabs.length > 0 && memberTabPanels.length > 0) {
        memberTabs.forEach(function (tab) {
            tab.addEventListener("click", function () {
                const target = tab.getAttribute("data-tab");

                activateMemberTab(target);

                if (target) {
                    history.replaceState(null, "", "#tab-" + target);
                }
            });
        });

        const hashTab = window.location.hash.replace("#tab-", "");
        if (hashTab) {
            activateMemberTab(hashTab);
        }
    }


    const packageSelect = document.getElementById("packageSelect");
    const durationPreview = document.getElementById("durationPreview");
    const sessionPreview = document.getElementById("sessionPreview");
    const pricePreview = document.getElementById("pricePreview");
    const paymentAmountInput = document.getElementById("paymentAmountInput");

    function formatMoney(value) {
        const number = Number(value || 0);
        return number.toLocaleString("vi-VN") + " đ";
    }

    if (packageSelect) {
        packageSelect.addEventListener("change", function () {
            const selected = packageSelect.options[packageSelect.selectedIndex];

            const price = selected.getAttribute("data-price") || "";
            const duration = selected.getAttribute("data-duration") || "";
            const sessions = selected.getAttribute("data-sessions") || "0";

            if (durationPreview) {
                durationPreview.value = duration ? duration + " ngày" : "";
            }

            if (sessionPreview) {
                sessionPreview.value = sessions && Number(sessions) > 0 ? sessions + " buổi" : "Không có PT";
            }

            if (pricePreview) {
                pricePreview.value = price ? formatMoney(price) : "";
            }

            if (paymentAmountInput) {
                paymentAmountInput.value = price || 0;
            }
        });
    }
});