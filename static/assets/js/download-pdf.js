function print_card(id, filename, parameters = false) {
  if (parameters) {
    let monthname = $("#month-name").text().trim();
    let yearname = $("#year-name").text().trim();
    filename = `Voucher-${monthname}-${yearname}`;
  }

  if (filename) {
    // console.log(selected_employee);
    let card = document.getElementById(id);
    html2pdf()
      .set({
        margin: [15, 40, 15, 40],
        filename: filename,
        image: { type: "jpeg", quality: 1 },
        html2canvas: {
          dpi: 192,
          scale: 4,
          letterRendering: true,
          useCORS: true,
        },
      })
      .from(card)
      .save();
  }
}
