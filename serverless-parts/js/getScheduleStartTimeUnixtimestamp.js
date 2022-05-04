module.exports = () => {
    /**
     * Get the Unixtimestamp for tomorrow.
     * This is used by the Appflow TriggerConfig -> TriggerProperties -> ScheduleStartTime
     *
     * Reference: https://www.serverless.com/framework/docs/providers/openwhisk/guide/variables#reference-variables-in-javascript-files
     */
    var d = new Date();
    d.setDate(d.getDate() + 1);
    d.setHours(2, 0, 0);
    d.setMilliseconds(0);

    return d.getTime() / 1000
}