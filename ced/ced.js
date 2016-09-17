function add_aspect() {
    $("#add_definition_panel").removeClass("hidden");
    $("#add_aspect_button").addClass("hidden");
}

function cancel_add_definition() {
    $("#add_definition_panel").addClass("hidden");
    $("#add_aspect_button").removeClass("hidden");
}

function on_xml_load(xml_data) {
    var core_xml = $(xml_data);

    core_xml.find("descriptor").each(function(didx, descriptor) {
        $descriptor = $(descriptor);

        console.log("Descriptor: " + $descriptor.attr("name"));

        $descriptor.find("feature").each(function(fidx, feature) {
            $feature = $(feature);

            console.log("\tFeature: " + $feature.attr("name") + "- Cost: " + $feature.attr("cost"));
        });
    });
}

function main() {
    $.ajax({
        url: "core.xml"
    }).done(on_xml_load);
}

main();
