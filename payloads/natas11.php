<?php 
$defaultdata = array("showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';
    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }
    return $outText;
}

function find_repeating_key($long_key) {
    // Get first 4 characters and keep eDWo as is
    $key = substr($long_key, 0, 4);
    // echo "Original key: $key\n";
    return $key;  // Return eDWo without rotation
}

$cookie = $argv[1] ?? null;
if (!$cookie) {
    exit(1);
}

$cookie = str_replace(' ', '+', $cookie);
$cipher_text = base64_decode($cookie);
$org_data = json_encode($defaultdata);

$full_key = xor_encrypt($org_data, $cipher_text);
// echo "Full key: $full_key\n";
$key = find_repeating_key($full_key);
// echo "Key: $key\n";
$spoof_data = json_encode(array(
    "showpassword" => "yes",
    "bgcolor" => "#ffffff"
));

$new_cookie = xor_encrypt($spoof_data, $key);
echo base64_encode($new_cookie);
?>